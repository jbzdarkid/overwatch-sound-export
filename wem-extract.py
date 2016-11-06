import os # system, stat, path.isfile, remove, listdir, devnull
import subprocess # call, STDOUT
from shutil import move
from hashlib import md5
from csv import reader

# Loading the config.
from sys import version_info
if version_info.major == 2:
    import ConfigParser as configparser
elif version_info.major == 3:
    import configparser
else:
    raise Exception("Unknown version:", version_info)
config = configparser.ConfigParser()
config.read("settings.conf")

print "Overwatch wem extractor v0.4"
# get hash storage
hashStorage = {}
with open(config.get("paths", "important"), "r") as csvfile:
    hashreader = reader(csvfile, delimiter=",")
    for row in hashreader:
        hashStorage[row[0]] = row[1]
with open(config.get("paths", "noise"), "r") as csvfile:
    hashreader = reader(csvfile, delimiter=",")
    for row in hashreader:
        hashStorage[row[0]] = "noise/"

def _name(hash):
    name = config.get("paths", "exported")
    if hash in hashStorage:
        name += hashStorage[hash]
    if name[-1] == "/":
        name += hash # File is not transcribed
    # Transcriptions (and hashes) have no extension
    return name + ".ogg"

def play(file):
    file = file.replace("/", "\\") # Windows slashes
    # Windows equivalent of unix open, i.e. will start playing
    if os.system(file) != 0:
        raise OSError
        # Ideally dont have this error print out

    try:
        from SendKeys import SendKeys
        from time import sleep
        sleep(0.1)
        SendKeys("%{TAB}") # Alt-Tab
    except ImportError:
        pass
    
def categorize_unknown(hash, file):
    play(file)
    while 1:
        try:
            code = raw_input().strip().lower()
        except KeyboardInterrupt:
            code = "x"
        if code == "?" or code == "":
            print "n - Categorize as noise"
            print "r - Re-listen"
            print "s - Skip"
            print "? - Print this help"
            print "x - Exit"
            print "Any other value - Categorize with value as path"
            continue
        elif code.lower() == "s":
            return
        elif code.lower() == "r":
            play(file)
            continue
        elif code.lower() == "x":
            os.remove(file)
            raise StopIteration
        elif code.lower() == "n":
            log = open(config.get("paths", "noise"), "a")
            log.write(hash + "\n")
            log.close()
            hashStorage[hash] = "noise/"
            break
        else:
            if not code.endswith("/"):
                code = code + "/"
            log = open(config.get("paths", "important"), "a")
            log.write(hash + "," + code + "\n")
            log.close()
            hashStorage[hash] = hash + "," + code + "\n"
            break

def transcribe_file(hash, path):
    file = config.get("paths", "exported") + path + hash + ".ogg"
    play(file)
    while 1:
        try:
            code = raw_input().strip().lower()
        except KeyboardInterrupt:
            code = "x"
        if code == "?" or code == "":
            print "n - Categorize as noise"
            print "r - Re-listen"
            print "s - Skip"
            print "? - Print this help"
            print "x - Exit"
            print "Any other value - Transcribe as value"
            print "Note: If value contains a / then"
            print "it will override the directory"
            continue
        elif code.lower() == "s":
            return path
        elif code.lower() == "r":
            play(file)
            continue
        elif code.lower() == "x":
            raise StopIteration
        else:
            code = code.lower().replace(" ", "_")
            # Remove non filename-safe characters. Credit to Vinko Vrsalovic:
            # http://stackoverflow.com/q/295135
            import string
            valid_chars = "-_.()/%s%s" % (string.ascii_letters, string.digits)
            code = "".join(c for c in code if c in valid_chars)
            if "/" in code:
                return code
            else:
                return path + code

folder = config.get("paths", "casc")
# run through the casc folder
try:
    dirs = os.listdir(folder)
    for i in xrange(len(dirs)):
        print '%0.2f%%' % (100.0*i/len(dirs))
        dir = dirs[i]
        for file in os.listdir(folder+"/"+dir):
            path = folder+"/"+dir+"/"+file
            contents = open(path, "r").read()
            # Ignore if first line doesn't contain wave headers
            if "WAVEfmt" not in contents:
                continue
            # Ignore if file is smaller than the minimum size (default 10k)
            if os.stat(path).st_size < int(config.get("default", "min_size")):
                continue
            # calculate hash from original file contents
            hash = md5(contents).hexdigest()
            if hash in hashStorage and os.path.isfile(_name(hash)):
                continue # File already converted

            # Convert to ogg using ww2ogg
            subprocess.call([
                    config.get("paths", "tools")+"ww2ogg.exe",
                    path,
                    "--pcb",
                    config.get("paths", "tools")+"packed_codebooks_aoTuV_603.bin"
                ],
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT)
            path = path.replace(".xxx", ".ogg")
            # If conversion fails, a file won't be created
            if not os.path.isfile(path):
                continue
            # Use revorb to fix potential problems
            subprocess.call([
                config.get("paths", "tools")+"revorb.exe", path], 
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT)
            if hash not in hashStorage: # New file
                categorize_unknown(hash, path)
            try:
                move(path, _name(hash))
            except IOError:
                pass
except StopIteration: # User wants to stop categorizing files
    pass

# Start transcription
lines_transcribed = 0
done_transcribing = False
sounds = []
with open(config.get("paths", "important"), "r") as csvfile:
    hashreader = reader(csvfile, delimiter=",")
    prev_path = ""
    for hash, path in hashreader:
        if path[-1] != "/": # Already transcribed
            lines_transcribed += 1
        elif done_transcribing: # User requested stop
            pass
        else:
            if path != prev_path:
                print path # Warn the user that we're in a new dir
                prev_path = path
            try:
                path = transcribe_file(hash, path)
                lines_transcribed += 1
            except StopIteration:
                done_transcribing = True
            except OSError:
                print "Corrupt path removed."
                continue
        sounds.append([path, hash])
sounds.sort()

with open(config.get("paths", "important"), "w") as csvfile:
    csvfile.write("\n".join([row[1]+","+row[0] for row in sounds])+"\n")

noises = []
with open(config.get("paths", "noise"), "r") as csvfile:
    hashreader = reader(csvfile, delimiter=",")
    for row in hashreader:
        noises.append(row[0])
noises.sort()
with open(config.get("paths", "noise"), "w") as csvfile:
    csvfile.write("\n".join(noises)+"\n")

readme = open("README.md").read().split("\n")
readme[0] = "[![Progress](https://img.shields.io/badge/Progress-%d%%25-green.svg)]()" % (100.0 * lines_transcribed/len(sounds) * i / len(dirs))
with open("README.md", "w") as f:
    f.write("\n".join(readme))
