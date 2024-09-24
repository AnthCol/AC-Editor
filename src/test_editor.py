from src.ac_editor import is_valid_vim

VALID_VIM_ANSWERS = {
    "h"   : "([1-9]+[0-9]*)*h",
    "j"   : "([1-9]+[0-9]*)*j", 
    "k"   : "([1-9]+[0-9]*)*k", 
    "l"   : "([1-9]+[0-9]*)*l", 
    "i"   : "i", 
    "A"   : "A", 
    "^"   : "\\^", 
    "$"   : "\\$", 
    "gg"  : "gg", 
    "G"   : "G", 
}

def test_is_valid_vim_h_good():
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
        "0h",
        "h1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_j_good():
    answer = VALID_VIM_ANSWERS["j"]
    tests = [
        "j",
        "20j",
        "1234567890j"
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_j_bad():
    answer = None
    tests = [
        "+j",
        "1234567890",
        "0j",
        "j1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_k_good():
    answer = VALID_VIM_ANSWERS["k"]
    tests = [
        "k",
        "20k",
        "1234567890k"
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_k_bad():
    answer = None
    tests = [
        "+k",
        "1234567890",
        "0k",
        "k1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_l_good():
    answer = VALID_VIM_ANSWERS["l"]
    tests = [
        "l",
        "20l",
        "1234567890l"
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_l_bad():
    answer = None
    tests = [
        "+l",
        "1234567890",
        "0l",
        "l1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_l_good():
    answer = VALID_VIM_ANSWERS["i"]
    tests = [
        "i",
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_l_bad():
    answer = None
    tests = [
        "+i",
        "1234567890i",
        "1i",
        "0i"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_A_good():
    answer = VALID_VIM_ANSWERS["A"]
    tests = [
        "A",
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_A_bad():
    answer = None
    tests = [
        "+A",
        "1234567890A",
        "1A",
        "0A",
        "A1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_hat_good():
    answer = VALID_VIM_ANSWERS["^"]
    tests = [
        "^",
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_hat_bad():
    answer = None
    tests = [
        "+^",
        "1234567890^",
        "^1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_dollar_good():
    answer = VALID_VIM_ANSWERS["$"]
    tests = [
        "$",
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_dollar_bad():
    answer = None
    tests = [
        "+$",
        "1234567890$",
        "1$",
        "$1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_gg_good():
    answer = VALID_VIM_ANSWERS["gg"]
    tests = [
        "gg",
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_gg_bad():
    answer = None
    tests = [
        "+gg",
        "1gg",
        "gg1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)

def test_is_valid_vim_G_good():
    answer = VALID_VIM_ANSWERS["G"]
    tests = [
        "G",
    ]
    passed = True
    for test in tests:
        valid, regex = is_valid_vim(test) 
        passed &= (valid == True and regex == answer)
    assert(passed == True)

def test_is_valid_vim_quitnosave_bad():
    answer = None
    tests = [
        "+G",
        "1G",
        "G1"
    ]
    passed = True 
    for test in tests:
        valid, regex = is_valid_vim(test)
        passed &= (valid == False and regex == answer)
    assert(passed == True)
