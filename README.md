[![Progress](https://img.shields.io/badge/Progress-89%25-green.svg)]()
# Overwatch - Sound export
This usefool tool will extract all the sound files from Overwatch.

All sound files ©Blizzard 2016. Please do not redistribute them independently!

## Summary
1. Download this repository
1a. Install Python
2. Download the required tools
3. Extract CASC (data files)
4. Run Python Script

### 1. Download this repository
[Click this](https://github.com/jbzdarkid/overwatch-sound-export/archive/master.zip). Extract the zip file and take note of its location.

#### 1a. Install python
This project runs on Python 2.7. 3.x compatibility is planned, but until then please download python [from the official site](https://www.python.org/downloads/).

### 2. Download the required tools
* [CascView](http://www.zezula.net/en/casc/main.html) Extracts the raw sound files from the game
* [ww2ogg](https://github.com/hcs64/ww2ogg/releases/download/0.24/ww2ogg024.zip) Converts wem (the raw sound file format) to ogg, a lossless audio codec.
* [revorb](http://yirkha.fud.cz/progs/foobar2000/revorb.exe) Fixes some problems after the conversion.

Once downloaded, move these files into this repository's tools folder:

* ww2ogg.exe (from ww2ogg)
* packed_codebooks_aoTuV_603.bin (from ww2ogg)
* revorb.exe (from revorb)

### 3. Extract CASC (data files)
* Launch CascView.exe, select Open Storage -> Program Files/Overwatch.
* Extract the "CONTENT_KEY" folder into this repository's casc folder.
  * Skip encrypted files [WIP]
  * Select the option for "Don't show an error message. Continue extracting."

### 4. Run Python Script
* Double-click run_extract.bat.
* If an error crops up, right click on run_extract.bat -> Edit, and make sure the path to python.exe is correct. (compare it to the place where you installed Python 2.7)
* Then, run the batch file again.
* For any other problems, open an issue on github and I'll do my best to help.

## Bugs? Feature requests?
If there's anything wrong (typos in transcription, miscategorized files) please feel free to open a github issue, or make a pull request.
