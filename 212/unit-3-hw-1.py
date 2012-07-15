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

def parse(start_symbol, text, grammar):
    """Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure iff remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T'"""

    tokenizer = grammar[' '] + '(%s)'

    def parse_sequence(sequence, text):
        print "=>parse_sequence(%s, '%s')<=" % (sequence, text)
        result = []
        for atom in sequence:
            print 'parse_sequence, atom: %s' % (atom)
            tree, text = parse_atom(atom, text)
            print "parse_sequence, parse_atom %s returned tree: '%s' text: '%s'" % (atom, tree, text)
            if text is None:
                print 'parse_sequence, returning Fail'
                return Fail
            result.append(tree)
            print "parse_sequence, result: '%s'" % result
        return result, text

    @memo
    def parse_atom(atom, text):
        if atom in grammar:  # Non-Terminal: tuple of alternatives
            print "==>parse_atom('%s', '%s')<==" % (atom, text)
            for alternative in grammar[atom]:
                print "parse_atom, parse_sequence('%s', '%s')" % (alternative, text)
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom]+tree, rem
            print 'parse_atom, returning Fail'
            return Fail
        else:  # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            print "parse_atom, re.match('%s', '%s') returned %r" % \
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

def json_parse(text):
    return parse('value', text, JSON)

def test():
    r1 = json_parse('1')
    print '---->', r1
    assert r1 == (['value', ['number', ['int', '1']]], '')

    r2 = json_parse('-123')
    print '---->', r2
    assert r2 == (['value', ['number', ['int', '-123']]], '')

    r3 = json_parse('-123.456')
    print '---->', r3
    assert r3 == (['value', ['number', ['int', '-123'], ['frac', '.456']]], '')

    r4 = json_parse('-123.456e+789')
    print '---->', r4
    assert r4 == (
        ['value', ['number', ['int', '-123'], ['frac', '.456'], ['exp', 'e+789']]], '')

    r5 = json_parse('null')
    print '---->', r5
    assert r5 == (['value', 'null'], '')
    
    r6 = json_parse('true')
    print '---->', r6
    assert r6 == (['value', 'true'], '')
    
    r7 = json_parse('false')
    print '---->', r7
    assert r7 == (['value', 'false'], '')

    r8 = json_parse('[1]')
    print '---->', r8
    assert r8 == (['value', ['array', '[', ['elements', ['value', ['number', ['int', '1']]]], ']', ]], '')

    r9 = json_parse('"testing"')
    print '---->', r9
    assert r9 == (['value', ['string', '"testing"']], '')

    r10 = json_parse('[1, 2, 3]')
    print '---->', r10
    assert r10 == (['value', ['array', '[',
        ['elements', ['value', ['number', ['int', '1']]], ',',
        ['elements', ['value', ['number', ['int', '2']]], ',',                        
        ['elements', ['value', ['number', ['int', '3']]]]]], ']']], '')
                            
    r11 = json_parse('["testing", 1, 2, 3]')
    print '---->', r11
    assert r11 == (                      
                       ['value', ['array', '[', ['elements', ['value', 
                       ['string', '"testing"']], ',', ['elements', ['value', ['number', 
                       ['int', '1']]], ',', ['elements', ['value', ['number', 
                       ['int', '2']]], ',', ['elements', ['value', ['number', ['int', '3']]]]]]], ']']], '')

    r12 = json_parse('{"age": 21, "state" : "CO", "occupation":"rides the rodeo"}')
    print '---->', r12
    assert r12 == (
                      ['value', ['object', '{', ['members', ['pair', ['string', '"age"'], 
                       ':', ['value', ['number', ['int', '21']]]], ',', ['members', 
                      ['pair', ['string', '"state"'], ':', ['value', ['string', '"CO"']]], 
                      ',', ['members', ['pair', ['string', '"occupation"'], ':', 
                      ['value', ['string', '"rides the rodeo"']]]]]], '}']], '')

    r13 = json_parse('[]')
    print '---->', r13
    assert r13 == (['value', ['array', '[', ']']], '')

    r14 = json_parse('[ ]')
    print '---->', r14
    assert r14 == (['value', ['array', '[', ']']], '')
    
    r15 = json_parse('{}')
    print '---->', r15
    assert r15 == (['value', ['object', '{', '}']], '')

    r16 = json_parse('{ }')
    print '---->', r16
    assert r16 == (['value', ['object', '{', '}']], '')

    return 'tests pass'
    
def p(gr):
    for k, v in gr.items():
        print '%s => %s' % (k, v)
p(JSON)

test()
#p(G)
#print(parse('Exp', '3*x + b', G))
#print test()
