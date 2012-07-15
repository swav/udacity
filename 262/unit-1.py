def myfirst_yoursecond(p, q):
    p_l = p.split(' ')
    q_l = q.split(' ')
    print 'p[0]: {0}, q[1]: {1}'.format(p_l[0], q_l[1])
    return (p_l[0] == q_l[1])

def test_myfirst_yoursecond():
    assert myfirst_yoursecond('grace hopper', 'will grace') 
    assert myfirst_yoursecond('grace hopper', 'will x') is not True
    assert myfirst_yoursecond('aa', 'bb aa')
    assert myfirst_yoursecond('aa', 'bb aax') is not True
    assert myfirst_yoursecond('x', 'y z') is not True
    #myfirst_yoursecond('x', 'y')
    
    print 'tests pass'


#test()

import re

def re_1(string):
    regexp = r"[a-z][a-z]|[0-9]+"
    return re.findall(regexp, string)

def test_re_1():
    assert re_1("ab") == ["ab"]
    assert re_1("1") == ["1"]
    assert re_1("123") == ["123"]
    assert re_1("a") != ["a"]
    assert re_1("abc") != ["abc"]
    assert re_1("abc123") != ["abc123"]
    
    print "all tests pass"

# test_re_1()

edges_1 = {(1, 'a') : 2,
         (2, 'a') : 2,
         (2, '1') : 3,
         (3, '1') : 3}

accepting = [1]

edges_q_star = \
{(1, ''): 1,
 (1, 'q'): 1
}

def fsmsim(string, current, edges, accepting):
    print "current: {1}, str: '{0}'".format(string, current)
    if string == "":
        return current in accepting
    else:
        letter = string[0]
        # Is there a valid edge?
        # If so, take it.
        if (current, letter) in edges:
            return fsmsim(string[1:], edges[(current, letter)], edges, accepting)
        else:
        # If not, return False.
            return False
        
def test_fsmsim_q_star():
    assert fsmsim("", 1, edges, accepting) == True
    assert fsmsim("q", 1, edges, accepting)
    assert fsmsim("qq", 1, edges, accepting) == True
    assert fsmsim("qqq", 1, edges, accepting) == True
    assert fsmsim("qp", 1, edges, accepting) == False
    print "all tests passed"

#test_fsmsim_q_star()
edges_ab_cd_opt = {(1, 'a'): 2,
                   (1, 'b'): 2,
                   #(2, ''): 3,
                   (2, 'c'): 3,
                   (2, 'd'): 3}
accepting_ab_cd_opt = [2,3]
def test_fsmsim_ab_cd_opt():
    assert fsmsim("a",1,edges_ab_cd_opt,accepting_ab_cd_opt)
    assert fsmsim("b",1,edges_ab_cd_opt,accepting_ab_cd_opt)
    assert fsmsim("ad",1,edges_ab_cd_opt,accepting_ab_cd_opt)
    assert fsmsim("ac", 1, edges_ab_cd_opt,accepting_ab_cd_opt)
    assert fsmsim("e",1,edges_ab_cd_opt,accepting) == False
    assert fsmsim("ae",1,edges_ab_cd_opt,accepting) == False
    print 'all tests passed'
    
#test_fsmsim_ab_cd_opt()

def sumnum(sentence):
    nums = re.findall(r"[0-9]+", sentence)
    sum = 0
    for n in nums:
        sum += int(n)

    return sum


