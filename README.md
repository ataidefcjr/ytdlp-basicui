# ****INSTALLATION****
### Make sure that you have Python and Git installed.
* `Windows users:` 
```
winget install python
winget install Git.Git
```
or manualy download and install from official websites.
* `Linux users:` 
```
sudo apt update
sudo apt install python3 git -y
```
**`Note:`** If your Linux system uses a different package manager such as `dnf` (Fedora), `pacman` (Arch Linux), or another, adjust the above commands according to your package manager's syntax.

### Once you have ensured Python and Git are installed:
```
git clone https://github.com/ataidefcjr/ytdlp-basicui
cd ytdlp-basicui
pip install -r requirements.txt
python create.py
```
#### `create.py` is used to create desktop shortchut.
**`Note:`** If you do not want to create the desktop shortcut or if it does not work, you can add it manually or run `main.py` directly each time.

## USAGE
You just need to enter the URL of the video you want *(separate multiple URLs by line break)*, select the output folder and click **`download`**.