WINDOW_EVENTS = {
    "new" : lambda event: new(), 
    "load" : lambda event: load(),
    "save" : lambda event: save(),
    "save_as" : lambda event: save_as(), 
    "close" : lambda event: close(), 
    "tab_change" : lambda event: tab_change(),
    "vim" : lambda event: vim(), 
    "esc" : lambda event: esc(), 
    "ret" : lambda event: ret(),
    "back" : lambda event: back()
}

VIM_EVENTS = {

}


