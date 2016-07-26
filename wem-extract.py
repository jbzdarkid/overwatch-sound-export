import os, subprocess, shutil, hashlib, csv, pprint, sys, json

print "Overwatch wem extractor v0.3"
# get config
with open('config.json') as data_file:
    config = json.load(data_file)
counter = 1
unknown = 0
# get hash storage
hashStorage = {}
with open(config["paths"]["important"], 'r') as csvfile:
    hashreader = csv.reader(csvfile, delimiter=',')
    for row in hashreader:
        hashStorage[row[0]] = row[1]
with open(config["paths"]["noise"], 'r') as csvfile:
    hashreader = csv.reader(csvfile, delimiter=',')
    for row in hashreader:
        hashStorage[row[0]] = 'noise/'+row[1]

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
            sys.exit(0)
        elif code.lower() == "n":
            log = open(config["paths"]["noise"], 'a')
            log.write(hash + ',' + file.replace(config["paths"]["exported"], "") + "\n")
            log.close()
            break
        else:
            if not code.endswith("/"):
                code = code + "/"
            log = open(config["paths"]["important"], 'a')
            log.write(hash + ',' + file.replace(config["paths"]["exported"], code) + "\n")
            log.close()
            break

folder = config["paths"]["casc"]
# run through the casc folder
for dir in os.listdir(folder):
    for file in os.listdir(folder+'/'+dir):
        # grab all the files
        if not file.endswith(".xxx"):
            continue
        path = folder+'/'+dir+'/'+file
        with open(path, 'r') as f:
            # Ignore if first line doesn't contain wave headers
            if "WAVEfmt" not in f.readline()[:20]:
                continue
            # show some progress
            if counter % 100 == 0:
                print counter
            counter = counter + 1
            if os.stat(path).st_size < 10 * 1024:
                continue
            # convert to ogg
            FNULL = open(os.devnull, 'w')
            subprocess.call(config["paths"]["tools"]+'ww2ogg.exe '+path+' --pcb '+config["paths"]["tools"]+'packed_codebooks_aoTuV_603.bin', stdout=FNULL, stderr=subprocess.STDOUT)
            # if convert was successful
            if os.path.isfile(path.replace(".xxx", ".ogg")):
                temp_path = config["paths"]["exported"]+str(counter)+".ogg"
                shutil.move(path.replace(".xxx", ".ogg"), temp_path)
                # fix ogg
                subprocess.call(config["paths"]["tools"]+'revorb.exe '+temp_path, stdout=FNULL, stderr=subprocess.STDOUT)
                # check against hash storage
                hash = hashlib.md5(f.read()).hexdigest()
                if hash in hashStorage:
                    # move to a nice folder
                    shutil.move(temp_path, config["paths"]["exported"]+hashStorage[hash])
                else:
                    # add hash to the unknowns list
                    categorize_unknown(hash, temp_path)
