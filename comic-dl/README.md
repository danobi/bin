comic-dl
=========
This script downloads comics from `readcomics.tv`.


Usage
------
`./main.py -c comic_name`

where `comic_name` is the comic name in the URL. For example, if you want to read Ninjak at `http://www.readcomics.tv/comic/ninjak-2015`, `comic_name` is `ninjak-2015`.

By default, `comic-dl` downloads all existing issues. `comic-dl` also makes an effort to avoid redownloading existing issues/pages.

`comic-dl` also downloads the specified comic to a new folder in the current directory.


TODO
-----
[ ] cmd line arg for download directory

[ ] cmd line arg for downloading specific issue #


Disclaimer
-----------
**Please** be respectful to `readcomics.tv`. Don't waste their bandwidth by being wasteful.
