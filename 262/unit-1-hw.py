def nfsmsim(string, current, edges, accepting):
    print 'string: {0}'.format(string)
    if len(string) == 0:
        return current in accepting
    else:
        next_ = edges[(current, string[0])
        return nfsmsim(string[1:], ,edges, accepting)


edges = {(1, 'a') : [2, 3],
         (2, 'a') : [2],
         (3, 'b') : [4, 3],
         (4, 'c') : [5]}

accepting = [2, 5]

def test():
    assert nfsmsim("abc", 1, edges, accepting)
    print "all tests pass"
    
test()
    
print "Test case 2 passed: " + str(nfsmsim("aaa", 1, edges, accepting) == True) 
print "Test case 3 passed: " + str(nfsmsim("abbbc", 1, edges, accepting) == True) 
print "Test case 4 passed: " + str(nfsmsim("aabc", 1, edges, accepting) == False) 
print "Test case 5 passed: " + str(nfsmsim("", 1, edges, accepting) == False) 
