[![Progress](https://img.shields.io/badge/Progress-0%25-green.svg)]()
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
This project runs on Python 2.7 or 3.6. Python is available [from the official site](https://www.python.org/downloads/).

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
* If CascView asks for a ListFile, just select 'Ok'.
* Right click on the "unknown" folder and hit extract
* Select the option for "Delete the local file and continue extracting"
* Hit OK, then wait 30 minutes or so.

### 4. Run Python Script
* Double-click run_extract.bat.
* If an error crops up, right click on run_extract.bat -> Edit, and make sure one of the paths to python.exe is correct. (compare it to the place where you installed Python)
* Then, run the batch file again.
* For any other problems, open an issue on github and I'll do my best to help.

## Bugs? Feature requests?
If there's anything wrong (typos in transcription, miscategorized files) please feel free to open a github issue, or make a pull request.
