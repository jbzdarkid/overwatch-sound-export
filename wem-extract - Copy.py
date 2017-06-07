from __future__ import print_function
import os # system, stat, path.isfile, remove, listdir, devnull
import subprocess # call, STDOUT
from shutil import move
from hashlib import md5
from csv import reader

print("Overwatch wem extractor v0.4")
# get hash storage
categorizations = {}
with open("data/categorizations.csv", "r") as csvfile:
    hashreader = reader(csvfile, delimiter=",")
    for row in hashreader:
        categorizations[row[0]] = row[1]
transcriptions = {}
with open("data/transcriptions.csv", "r") as csvfile:
    hashreader = reader(csvfile, delimiter=",")
    for row in hashreader:
        transcriptions[row[0]] = row[1]

def _name(hash):
    path = "exported/"
    if hash in transcriptions:
        path += transcriptions[hash]
    if path.endswith("/"):
        path += hash # File is not transcribed
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
    
def categorize(hash, file):
    play(file)
    while 1:
        try:
            code = raw_input().strip().lower()
        except KeyboardInterrupt:
            code = "x"
        if code == "?" or code == "":
            print("n - Categorize as noise")
            print("v - Categorize as voice")
            print("r - Replay")
            print("s - Skip")
            print("? - Print this help")
            print("x - Exit")
            print("Any other value - Categorize with value as path")
            continue
        elif code.lower() == "s":
            return
        elif code.lower() == "r":
            play(file)
            continue
        elif code.lower() == "x":
            os.remove(file)
            raise StopIteration
        else:
            if code.lower() == "n":
                path = "noise/" + hash
                transcriptions[hash] = path
                with open("data/transcriptions.csv", "a") as saved_transcriptions:
                    saved_transcriptions.write(hash, path)
            elif code.lower() == "v":
                path = "voice/" + hash
                transcriptions[hash] = path
                with open("data/transcriptions.csv", "a") as saved_transcriptions:
                    saved_transcriptions.write(hash, path)
            else:
                path = code[:-1] if code.endswith("/") else code
                categorizations[hash] = path
                with open("data/categorizations.csv", "a") as saved_categorizations:
                    saved_categorizations.write(hash, path)
            break

def transcribe(hash, path):
    file = "exported/%s/%s.ogg" % (path, hash)
    play(file)
    while 1:
        try:
            code = raw_input().strip().lower()
        except KeyboardInterrupt:
            code = "x"
        if code == "?" or code == "":
            print("n - Categorize as noise")
            print("v - Categorize as voice")
            print("r - Replay")
            print("s - Skip")
            print("? - Print this help")
            print("x - Exit")
            print("Any other value - Transcribe as value")
            print("Note: If value contains a / then")
            print("it will override the directory")
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
            path = "".join(c for c in code if c in valid_chars)
            if "/" in code:
                return code
            else:
                return path + code

# run through the casc folder
# FIXME: Multithreading
try:
    for root, dirs, files in os.walk("casc\\unknown\\"):
        print(root)
        for file in files:
            path = root+os.sep+file
            try:
                contents = open(path).read()
                print(len(contents))
            except UnicodeDecodeError:
                continue
            # Ignore if first line doesn't contain wave headers
            if "WAVEfmt" not in contents:
                continue
            print(path)
            
            # Calculate hash from original file contents
            hash = md5(contents).hexdigest()
            if hash in transcriptions or hash in categorizations:
                print('<143>')
                continue # File already converted
            
            # Convert to ogg using ww2ogg
            subprocess.call([
                    "tools\\ww2ogg.exe",
                    path,
                    "--pcb",
                    "tools\\packed_codebooks_aoTuV_603.bin"
                ],
                stdout=subprocess.STDOUT,# open(os.devnull, "w"),
                stderr=subprocess.STDOUT)
            print('<154>')
            path = path.replace(".xxx", ".ogg")
            
            # If conversion fails, a file won't be created
            if not os.path.isfile(path):
                continue
            
            # Use revorb to fix potential problems
            subprocess.call([
                "tools/revorb.exe", path], 
                stdout=open(os.devnull, "w"),
                stderr=subprocess.STDOUT)
            print(hash)
            if hash not in categorizations: # New file
                categorize(hash, path)
            try:
                move(path, "exported/" + categorizations[hash])
            except IOError:
                pass
except StopIteration: # User wants to stop categorizing files
    pass

# Start transcription
with open("data/categorizations.csv", "r") as csvfile:
    hashreader = reader(csvfile, delimiter=",")
    prev_path = ""
    for hash, path in hashreader:
        if path != prev_path:
            print(path) # Warn the user that we're in a new dir
            prev_path = path
        try:
            path = transcribe_file(hash, path)
        except StopIteration:
            break
        except OSError:
            print("Corrupt path removed")
            continue
        transcriptions[hash] = path
        with open("data/transcriptions.csv", "a") as saved_transcriptions:
            saved_transcriptions.write(hash, path)

progress = 0.0
# progress = 100.0 * len(transcriptions) / len(sounds) * i / len(dirs)
readme = open("README.md").read().split("\n")
readme[0] = "[![Progress](https://img.shields.io/badge/Progress-%d%%25-green.svg)]()" % progress
with open("README.md", "w") as f:
    f.write("\n".join(readme))
