import os, subprocess, shutil, hashlib, csv, sys, json

print "Overwatch wem extractor v0.3"
# get config
with open('config.json') as data_file:
    config = json.load(data_file)
# get hash storage
hashStorage = {}
with open(config["paths"]["important"], 'r') as csvfile:
    hashreader = csv.reader(csvfile, delimiter=',')
    for row in hashreader:
        hashStorage[row[0]] = row[1]
with open(config["paths"]["noise"], 'r') as csvfile:
    hashreader = csv.reader(csvfile, delimiter=',')
    for row in hashreader:
        hashStorage[row[0]] = 'noise/'

def play(file):
    file = file.replace("/", "\\") # Windows slashes
    os.system(file) # Windows equivalent of 'open', i.e. will start playing

def categorize_unknown(hash, file):
    play(file)
    while 1:
        try:
            code = raw_input()
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
            log = open(config["paths"]["noise"], 'a')
            log.write(hash + "\n")
            log.close()
            break
        else:
            if not code.endswith("/"):
                code = code + "/"
            log = open(config["paths"]["important"], 'a')
            log.write(hash + ',' + code + "\n")
            log.close()
            break

folder = config["paths"]["casc"]
# run through the casc folder
try:
    dirs = os.listdir(folder)
    for i in xrange(len(dirs)):
        print '%.02f%%' % (100.0*i/len(dirs))
        dir = dirs[i]
        for file in os.listdir(folder+'/'+dir):
            # grab all the files
            if not file.endswith(".xxx"):
                continue
            path = folder+'/'+dir+'/'+file
            contents = open(path, 'r').read()
            # Ignore if first line doesn't contain wave headers
            if "WAVEfmt" not in contents:
                continue
            # Ignore if file is smaller than the minimum size (default 10k)
            if os.stat(path).st_size < config["min_size"]:
                continue
            # calculate hash from original file contents
            hash = hashlib.md5(contents).hexdigest()
            if hash in hashStorage and os.path.isfile(_name(hash)):
                continue # File already converted

        # Convert to ogg using ww2ogg
        subprocess.call([
            config["paths"]["tools"]+'ww2ogg.exe', path,
            '--pcb', config["paths"]["tools"]+'packed_codebooks_aoTuV_603.bin'],
            stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)
        path = path.replace(".xxx", ".ogg")
        # If conversion fails, a file won't be created
        if not os.path.isfile(path):
            continue
        # Use revorb to fix potential problems
        subprocess.call([
            config["paths"]["tools"]+'revorb.exe', path], 
            stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT)

        # calculate hash from original file contents
        hash = hashlib.md5(contents).hexdigest()
        with open(folder+'/'+dir+'/'+file, 'r') as f:
            f.readline()
            contents2 = f.read()
            hash2 = hashlib.md5(contents2).hexdigest()
        if hash2 in hashStorage:
            f = open(config["paths"]["important"], 'r').read()
            g = open(config["paths"]["important"], 'w')
            g.write(f.replace(hash2, hash))
            g.close()
            f = open(config["paths"]["noise"], 'r').read()
            g = open(config["paths"]["noise"], 'w')
            g.write(f.replace(hash2, hash))
            g.close()
            continue
        # If hash is already known
        if hash in hashStorage:
            try:
                shutil.move(path, config["paths"]["exported"]+hashStorage[hash])
            except shutil.Error as e:
                if e.message.startswith("Destination path"):
                    continue # File already exists
                raise
        # Otherwise prompt user for categorization
        else:
            categorize_unknown(hash, path)
except StopIteration: # User wants to stop categorizing files, cleanup and shut down
