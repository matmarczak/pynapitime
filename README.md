# Pynapitime

Pynapitime is a scipt to download subtitles from napiprojekt.pl based on movie duration and fps of file. It differs from other programs that it can download subtitles automatically for files which are not in napiprojekt database yet.

### Requirements

Program needs **mediainfo** to be installed to work properly. Install mediainfo for your OS with instruction provided on [official page](https://mediaarea.net/en/MediaInfo/Download).


TODO:
* add recursive search to search files method
* block downloading subs when duration diffrence is too big
* add support for series
* remove uninformative assertions
* add threading to multiple subtitles downloading
* change prints to logging module
* resolve all pylama issues