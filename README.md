[![Progress](https://img.shields.io/badge/Progress-24%25-yellow.svg)]()
# Overwatch - Sound export
This usefool tool + tutorial gets you all the sound files extracted from the overwatch data files.

## Quick tutorial
1. Grab git contents
2. Get Tools
3. Get Python
4. Extract CASC
5. Run Python Script
6. Enjoy the sound files / contribute

### 1. Grab git contents
Just download & place in a folder of your choice.

### 2. Get Tools
This project depends on three tools.
* ww2ogg -> converts wem format to ogg. https://github.com/hcs64/ww2ogg/releases/download/0.24/ww2ogg024.zip
* revorb -> fixes ogg headers. http://yirkha.fud.cz/progs/foobar2000/revorb.exe
* casc tools -> extracts the raw files from overwatch. http://www.zezula.net/en/casc/main.html

Once downloaded, place the following files directly into the tools folder:

* ww2ogg -> ww2ogg.exe
* ww2ogg -> packed_codebooks_aoTuV_603.bin
* revorb.exe

(tools folder is projectfolder/tools)

### 3. Get Python
This project runs on Python 2.7.
Grab it from here: https://www.python.org/downloads/

### 4. Extract CASC
* Launch CascView.exe, select Open Storage -> Program Files/Overwatch. 
* Extract the "unknown" folder to this repo, in the /casc folder.  Be sure to hit the checkbox for "Delete the local file and continue extracting"

### 5. Run the script.
* Double-click run_extract.bat.
* If an error crops up, right click on run_extract.bat -> Edit, and make sure the path to python.exe is correct. (compare it to the place where you installed Python 2.7)
* Then, run the batch file again.

### 5a. Categorizing files
* If a file has an unknown hash (e.g. a new character's voice lines), the script will prompt you to categorize it. Type in a code and press enter to save the categorization:
** ? - Show this help
* Once done, please create a pull request with your modifications to the .csv files.
