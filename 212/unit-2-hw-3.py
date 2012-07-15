# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

#def longest_subpalindrome_slice(text):

def lss(text):   
    "Return (i, j) such that text[i:j] is the longest palindrome in text."

    starting_tuples = calc_pal_origins(text)

    all_p_lengths = []
    if starting_tuples:
        for st in starting_tuples:
            all_p_lengths.append(measure_p(text, st))
            
        return sorted(all_p_lengths, key=lambda x: x[1] - x[0])[-1]
    else:
        return (0, 0)

def calc_pal_origins(text):
    "returns a list of tuples of all palindrome center points (pairs of chars or triples)"
    res = []
    if len(text) == 2: #special case, for loop will never run
        if text[0].lower() == text[1].lower():
            res.append((0, 1))

    for i in range(1, len(text)-1):
        l = text[i-1].lower()
        c = text[i].lower()
        r = text[i+1].lower()
        #print 'i=%d, text[i-1]=%s text[i]=%s text[i+1]=%s' % (i, l, c, r )
        if l == r:
            res.append((i-1, i+1))
        elif l == c:
            res.append((i-1, i))
        elif c == r:
            res.append((i, i+1))
    return res

def measure_p(text, starting_tuple):
    l, r = starting_tuple
    print 'l=%d, r=%d'  % (l, r)
    while l >= 1 and r < len(text) - 1:
        if text[l - 1].lower() == text[r + 1].lower():
            l -= 1
            r += 1
        else:
            break
    return (l, r+1)
    
def test_calc_pal_origins():
    c = calc_pal_origins
    assert c('xx') == [(0, 1)]
    assert c('ab') == []
    assert c('aba') == [(0, 2)]
    assert c('abcbaba') == [(1, 3), (3, 5), (4, 6)]
    assert c('xxx') == [(0, 2)]
    assert c('xxxx') == [(0, 2), (1, 3)]
    assert c('xxxxx') == [(0, 2), (1, 3), (2, 4)]
    assert c('race carr') == [(7, 8)]
    assert c('racecar') == [(2, 4)]
    assert c('something rac e car going') == [(13,15)]
    assert c('Racecar') == [(2, 4)]
    return 'test passed'

def test_measure_p():
    m = measure_p
    assert m('xx', (0, 1)) == (0, 2)
    assert m('aba', (0, 2)) == (0, 3)
    assert m('abcbaba', (1, 3)) == (0, 5)
    assert m('abcbaba', (3, 5)) == (3, 6)
    assert m('abcbaba', (4, 6)) == (4, 7)
    assert m('xxxx', (0, 2)) == (0, 3)
    assert m('xxxx', (1, 3)) == (1, 4)
    assert m('xxxxx', (0, 2)) == (0, 3)
    assert m('xxxxx', (1, 3)) == (0, 5)
    assert m('xxxxx', (2, 4)) == (2, 5)
    assert m('Racecar', (2, 4)) == (0, 7)
    assert m('racecarx', (2, 4)) == (0, 7)
    assert m('something rac e car going', (13,15)) == (8, 21)
    
    return 'test_measure_p pass'
            
def test():
    L = lss #longest_subpalindrome_slice
    assert L('racecar') == (0, 7)
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('racecarx') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    assert L('mad am i ma dam.') == (0, 15)
    return 'tests pass'

print test_calc_pal_origins()
print test_measure_p()
print test()


    

