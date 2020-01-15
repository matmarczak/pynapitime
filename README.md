# Pynapitime

Pynapitime is a tool for downloading subtitles from napiprojekt.pl based on movie duration and fps.
It differs from other programs, that it downloads subtitles for files which hashes
are not in napiprojekt database yet.

Script can:
* Download subtitles based on movie duration
* Autodetect title and year
* Download subtitles for folders
* Download subtitles with hash from napiprojekt
* Override title and year if filename is malformed

For accurate subtitle match, query script needs full (preferably translated to PL) title and year. 
If no movies were found, try adding title and year manually with `--title "Some title" --year 2010` flags.

Requires python >= 3.6

### Requirements

According to `requirements.txt`

## Usage

1. Download projekt: `git clone https://github.com/matmarczak/pynapitime.git`
2. Install dependencies from requirements.txt file: `pip install -r requirements.txt`
3. Use script: `python pynapitime.py path/to/file.mkv`

#### Help

For help use `python pynapitime --help`
