# Pynapitime

Pynapitime is a tool for downloading subtitles from napiprojekt.pl based on movie duration and fps of file. It differs from other programs that it can download subtitles automatically for files which hashes are not in napiprojekt database yet.

Requires python >3.6

### Requirements

Program needs **mediainfo** to be installed to work properly. Install mediainfo for your OS with instruction provided on [official page](https://mediaarea.net/en/MediaInfo/Download).

## Usage

1. Download projekt: `git clone https://github.com/matmarczak/pynapitime.git`
2. Install dependencies from requirements.txt file: `pip install -r requirements.txt`
3. Use script: `python pynapitime.py`

#### Help

For help use `python pynapitime --help`
