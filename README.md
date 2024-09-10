# ac_editor
Welcome to ac_editor! 
This is a small, lightweight editor that I made for myself, intended to be used primarily for note-taking. 


## Tech 

<img src="./docs/images/python_logo.png" height=100/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="./docs/images/sqlite_logo.png" height=100/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<img src="./docs/images/tkinter_logo.gif" height=100>

## Motivation
I like using Notepad++, and I also like using Vim. While programming, I like to keep open a lightweight text editor alongside my IDE 
to take notes in. Most of the time this is Notepad++, but I find myself missing having Vim motions available. 
Therefore, I decided to make this small, lightweight text editor for me to take notes in, that supports a small subset of the 
Vim commands I use the most. 
<br><br>
<i>Why not make a plugin for Notepad++?</i><br>
While the thought did cross my mind, I eventually came to the conclusion that it might be better to just write my own editor from scratch, since I will get more experience with GUIs, databases, and writing/desigining projects from the ground up. 

## Supported Vim Commands

The subset of Vim commands supported by this editor are listed below:

```
- i         (enter INSERT mode)
- esc       (enter NORMAL mode)
- <NUM> h   (move cursor left NUM spaces)
- <NUM> j   (move cursor down NUM lines)
- <NUM> k   (move cursor up NUM lines)
- <NUM> l   (move cursor right NUM spaces)
- shift + a (move cursor to end of line and enter INSERT mode)
- shift + ^ (move cursor to start of line)
- shift + $ (move cursor to end of line)
```

## Limitations

- I have only tested this project on Windows. Key shortcuts may not work on other operating systems. 
- `VISUAL` mode is not currently supported. 
- Rebinding keys is not currently supported. 



