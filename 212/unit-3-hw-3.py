# ---------------
# User Instructions
#
# In this problem, you will be using many of the tools and techniques
# that you developed in unit 3 to write a grammar that will allow
# us to write a parser for the JSON language. 
#
# You will have to visit json.org to see the JSON grammar. It is not 
# presented in the correct format for our grammar function, so you 
# will need to translate it.

# ---------------
# Provided functions
#
# These are all functions that were built in unit 3. They will help
# you as you write the grammar.  Add your code at line 102.

from functools import update_wrapper
#from string import split
import re

def split(text, sep = None, maxsplit = -1):
    "Like str.split applied to text, but strips whitespace from each piece."
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]

def grammar(description, whitespace = r'\s*'):
    """
    Convert a description to a grammar. Each line is a rule for a
    non-terminal symbol; it looks like this:

        Symbol => A1 A2 ... | B1 B2 ... | C1 C2 ...

    where the right-hand side is one or more alternatives, separated by
    the '|' sign. Each alternative is a sequence of atoms, separated by
    spaces.  An atom is either a symbol on syme left-hand side, or it is a
    regular expression that will be passed to re.match to match a token.

    Notation for *, +, or ? not allowed in a rule alternative (but ok within a
    token). Use '\' to continue long lines. You must include spaces or tabs
    around '=>' and '|'. That's within the grammar description itself(...?). The
    grammar that gets defined allows whitespace between tokens by default or
    specify '' as the second argument to grammar() to disallow this (or supply
    any regular expression to describe allowable whitespace between
    tokens)."""
    G = {' ': whitespace}
    description = description.replace('\t', ' ') # no tabs!
    for line in split(description, '\n'):
        print 'line: \'%s\'' % (line)
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G
def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

def parse(start_symbol, text, grammar, verbose=False):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        if verbose: print "=>parse_sequence(%s, '%s')<=" % (sequence, text)
        result = []
        for atom in sequence:
            if verbose: print 'parse_sequence, atom: %s' % (atom)
            tree, text = parse_atom(atom, text)
            if verbose: print "parse_sequence, parse_atom %s returned tree: '%s' text: '%s'" % (atom, tree, text)
            if text is None:
                if verbose: print 'parse_sequence, returning Fail'
                return Fail
            result.append(tree)
            if verbose: print "parse_sequence, result: '%s'" % result
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            if verbose: print "==>parse_atom('%s', '%s')<==" % (atom, text)
            for alternative in grammar[atom]:
                if verbose: print "parse_atom, parse_sequence('%s', '%s')" % (alternative, text)
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            if verbose: print 'parse_atom, returning Fail'
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            if verbose: print "parse_atom, re.match('%s', '%s') returned %r" % \
                (tokenizer % atom, text, m)
            return Fail if (not m) else (m.group(1), text[m.end():])
    
    # Body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)

JSON_WRK = grammar(r"""
members => pair [,] members | pair
pair => string [:] value
value => string | number | object
number => int frac exp | int frac | int
object => [{] members [}]
array => [\[] elements [\]]
string => "[a-zA-Z_1-9\s]+"
int => [-+]?[0-9]+
frac => [.][0-9]+
exp => e[+]?[0-9]+
""", whitespace='\s*')

JSON = grammar(r"""
elements => value [,] elements | value
members => pair [,] members | pair
pair => string [:] value
value => string | number | object | array | true | false | null
number => int frac exp | int frac | int
object => [{] members [}] | [{] [}]
array => [\[] elements [\]] | [\[] [\]]
string => "[a-zA-Z_1-9\s]+"
int => [-+]?[0-9]+
frac => [.][0-9]+
exp => e[+]?[0-9]+
""", whitespace='\s*')

G = grammar(r"""
Exp => Term [+-] Exp | Term
Term => Factor [*/] Term | Factor
Factor => Funcall | Var | Num | [(] Exp [)]
Funcall => Var [(] Exps [)]
Exps => Exp [,] Exps | Exp
Var => [a-zA-Z_]\w*
Num => [-+]?[0-9]+([.][0-9]*)?
""")
HTML_TAG = grammar(r"""
text => string tag text | string
tag => simple_tag | complex_tag | bs_tag | gt
start_simple_tag => [<] \s*[a-zA-Z]+\s* [>]
end_tag => [<]\s*[\/] attrib [>]
simple_tag => start_simple_tag string end_tag
start_complex_tag => [<] \s*[a-zA-Z]+\s* attrib_item [>]
complex_tag => start_complex_tag string end_tag
bs_tag => [<] string [>]
attrib_item => \s*[a-zA-Z]+\s* [=] "[a-zA-Z_\.]+" attrib_item | \s*[a-zA-Z]+\s* [=] "[a-zA-Z_\.]+"
attrib => \s*[a-zA-Z]+\s*
value => "[a-zA-Z_\.]+"
string => [a-zA-Z0-9\n\.,'!?\s]+
gt => [>]
string_alt => [a-zA-Z0-9\n\.,'!?<>\s]+
""", whitespace='\s*')

##HTML_TAG1 = grammar(r"""
##text => string tag text | string
##tag => simple_tag | complex_tag | bs_tag | gt
##start_simple_tag => [<] attrib [>]
##end_tag => [<]\s*[\/] attrib [>]
##simple_tag => start_simple_tag string end_tag
##start_complex_tag => [<] attrib attrib_item [>]
##complex_tag => start_complex_tag string end_tag
##bs_tag => [<] string [>]
##attrib_item => attrib [=] value attrib_item | attrib [=] value
##attrib => \s*[a-zA-Z]+\s*
##value => "[a-zA-Z_\.]+"
##string => [a-zA-Z0-9\n\.,'!?\s]+
##gt => [>]
##string_alt => [a-zA-Z0-9\n\.,'!?<>\s]+
##""", whitespace='\s*')

##HTML_TAG0 = grammar(r"""
##text => string tag text | string
##tag => simple_tag | complex_tag
##start_simple_tag => [<] attrib [>]
##end_tag => [<]\s*[\/] attrib [>]
##simple_tag => start_simple_tag string end_tag
##start_complex_tag => [<] attrib attrib_item [>]
##complex_tag => start_complex_tag string end_tag
##attrib_item => attrib [=] value attrib_item | attrib [=] value
##attrib => \s*[a-zA-Z]+\s*
##value => "[a-zA-Z_\.]+"
##string => [a-zA-Z0-9\n\.,'!?\s]+
##""", whitespace='\s*')

#string => [a-zA-Z0-9\n\.,'!?<>\s]+ #including '<>' in string parses r3 ok, but breaks r1 & r2
def text_parse(text):
    return parse('text', text, HTML_TAG)

testtext1 = """
My favorite website in the world is probably 
<a href="www.udacity.com">Udacity</a>. If you want 
that link to open in a <b>new tab</b> by <let's say> default, you should when 2 > <b>3</b>
write <a href="www.udacity.com"target="_blank">Udacity</a>
instead!
"""
    
def test():
    r1 = text_parse(testtext1)
    print '\n---->', r1
    print '\n----> last item: ', r1[-1]
    #assert r1 == (['value', ['number', ['int', '1']]], '')
    
##    r2 = text_parse("""
##Okay, so you passed the first test case. <let's see> how you 
##handle this one. Did you know that 2 < 3 should return True? 
##So should 3 > 2. But 2 > 3 is always False.
##""")
##    print '---->', r2
    
##    r2 = text_parse("""
##It's not common, but we can put a LOT of whitespace into 
##our HTML tags. For example, we can make something bold by
##doing <         b           > this <   /b    >, Though I 
##don't know why you would ever want to.
##""")
##    print '---->', r2

def find_lists_starting_with(tag_names, tag_list):
    result = []
    #print '==>find_lists_starting_with:', tag_list, 'result:', result
    for tl in tag_list:
        if tl in tag_names:
            #print 'tl:', tl
            result.append(tag_list)
            #print 'result: ', result
        else:
            if isinstance(tl, list):
                l = find_lists_starting_with(tag_names, tl)
                if len(l):
                    #print 'l:', l
                    result = result + l
                    #print 'result:', result
            
        #if isinstance(tl, list):
    #print '==>exiting find_lists_starting_with:', tag_list, 'result:', result
    return result
 
def findtags(text):
    tags, rest = text_parse(text)
    #print 'tags:', tags
    #print 'rest:', rest
    #assert len(rest) == 0

    start_tags = find_lists_starting_with(('start_simple_tag', 'start_complex_tag'), tags)
    #print "start_complex_tag:", start_tags
    result = []
    for st in start_tags:
        #print 'st:', st
        if st[0] == 'start_simple_tag':
            result.append(''.join([s for s in st[1:]]))
        elif st[0] == 'start_complex_tag':
            result.append(''.join(build_complex_tag(st)))
    return result

def build_complex_tag(tag_def):
    result = []
    #print 'build_complex_tag', tag_def, 'result:', result
    for td in tag_def[1:]:
        if isinstance(td, list):
            result = result + build_complex_tag(td)
            #print 'isinstance result', result
        else:
            result.append(td)
            #print 'else result', result
    #print 'exiting build_complex_tag, result', result
    return result
    
print '-------------findtags------------'
print findtags(testtext1)

           
    
def test1():
    assert findtags(r1) == ['<a href="www.udacity.com">',
                            '<b>',
                            '<a href="www.udacity.com"target="_blank">']
    
