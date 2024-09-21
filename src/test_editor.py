from src.ac_editor import is_valid_vim

VALID_VIM_ANSWERS = {
    "h" : "([1-9]+[0-9]*)*h",
    "j" : "([1-9]+[0-9]*)*j", 
    "k" : "([1-9]+[0-9]*)*k", 
    "l" : "([1-9]+[0-9]*)*l", 
    "i" : "i", 
    "A" :"A", 
    "^" : "\\^", 
    "$" : "\\$", 
    ":w" : ":w", 
    ":q" : ":q", 
    ":wq" : ":wq", 
    ":q!" : ":q!", 
    "gg" : "gg", 
    "G" : "G", 
}

def test_is_valid_vim_h_good():
    # Command : Regex
    answer = VALID_VIM_ANSWERS["h"]
    tests = [
        "h",
        "20h",
        "1234567890h"
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_h_bad():
    answer = None
    tests = [
        "+h",
        "1234567890",
        "0h"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        print("printing valid: " + str(valid))
        passed &= (valid == False and regex == answer)
    assert(passed == True)


