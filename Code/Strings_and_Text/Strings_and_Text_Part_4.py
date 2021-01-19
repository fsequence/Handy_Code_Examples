
# Strings and Text Part 4
# =-=-=-=-=-=-=-=-=-=-=-=-


# 16) Reformatting Text to a Fixed Number of Columns, line 15
# 17) Handling HTML and XML Entities in Text, line 82
# 18) Tokenizing Text, line 164
# 19) Writing a Simple Recursive Descent Parser, line


# -------------------------------------------------------------------------


# 16) Reformatting Text to a Fixed Number of Columns


# You have long strings that you want to reformat so that they fill a
# user-specified number of columns.

# Use the textwrap module to reformat text for output. For example, suppose
# you have the following long string:


s = "Look into my eyes, look into my eyes, the eyes, the eyes, \
    the eyes, not around the eyes, don't look around the eyes, \
    look into my eyes, you're under."


# Here's how you can use the textwrap module to reformat it in various
# ways:


import textwrap

print(textwrap.fill(s, 70))
# Look into my eyes, look into my eyes, the eyes, the eyes, the eyes,
# not around the eyes, don't look around the eyes, look into my eyes,
# you're under.

print(textwrap.fill(s, 40))
# Look into my eyes, look into my eyes,
# the eyes, the eyes, the eyes, not around
# the eyes, don't look around the eyes,
# look into my eyes, you're under.

print(textwrap.fill(s, 40, initial_indent='    '))
#     Look into my eyes, look into my
# eyes, the eyes, the eyes, the eyes, not
# around the eyes, don't look around the
# eyes, look into my eyes, you're under.

print(textwrap.fill(s, 40, subsequent_indent='    '))
# Look into my eyes, look into my eyes,
#     the eyes, the eyes, the eyes, not
#     around the eyes, don't look around
#     the eyes, look into my eyes, you're
#     under.


# The textwrap module is a straightforward way to clean up text for
# printing--especially if you want the output to fit nicely on the
# terminal. On the subject of the terminal size, you can obtain it using
# os.get_terminal_size().


# For example:


import os
os.get_terminal_size().columns
# 80


# The fill() method has a few additional options that control how it
# handles tabs, sentence endings, and so on. Look at the documentation for
# the textwrap.TextWrapper class
# (http://docs.python.org/3.3/library/textwrap.html#textwrap.TextWrapper)
# for further details.


# 17) Handling HTML and XML Entities in Text


# You want to replace HTML or XML entities such as &entity; or &#code; with
# their corresponding text. Alternatively, you need to produce text, but
# escape certain characters ( e.g., <, >, or &).

# If you are producing text, replacing special characters such as < or > is
# relatively easy if you use the html.escape() function.


# For example:


s = 'Elements are written as "<tag>text</tag>".'
import html

print(s)
# Elements are written as "<tag>text</tag>".
print(html.escape(s))
# Elements are written as &quot;&lt;tag&gt;text&lt;/tag&gt;&quot;.

# Disable escaping of quotes
print(html.escape(s, quote=False))
# Elements are written as "&lt;tag&gt;text&lt;/tag&gt;".


# If you're trying to emit text as ASCII and want to embed character code
# entities for non-ASCII characters, you can use the
# errors='xmlcharrefreplace' argument to various I\O related functions to
# do it.


# For example:


s = 'Spicy Jalapeno'        # the n has an accent

s.encode('ascii', errors='xmlcharrefreplace')
# b'Spicy Jalape&#241;o'


# To replace entities in text, a different approach is needed. If you're
# actually processing HTML or XML, try using a proper HTML or XML parser
# first. Normally, these tools will automatically take care of replacing
# the values for you during parsing and you don't need to worry about it.

# If, for some reason, you've received bare text with some entities in it
# and you want them replaced manually, you can usually do it using various
# utility functions\methods associated with HTML or XML parsers.


# For example:


s = 'Spicy &quot;Jalape&#241;o&quot.'
from html.parser import HTMLParser
p = HTMLParser()

p.unescape(s)
'Spicy "Jalapeno".'         # n has accent

t = 'The prompt is &gt;&gt;&gt;'
from xml.sax.saxutils import unescape

unescape(t)
'The prompt is >>>'


# Proper escaping of special characters is an easily overlooked detail of
# generating HTML or XML. This is especially true if you're generating such
# output yourself using print() or other basic string formatting features.
# Using a utility function such as html.escape() is an easy solution.

# If you need to process text in the other direction, various utility
# functions, such as xml.sax.saxutils.unescape(), can help. However, you
# really need to investigate the use of a proper parser. For example, if
# processing HTML or XML, using a parsing module such as html.parser or
# xml.etree.ElementTree should already take care of details related to
# replacing entities in the input text for you.


# 18) Tokenizing Text


# You have a string that you want to parse left to right into a stream of
# tokens.

# Suppose you have a string of text such as this:


text = 'foo = 23 + 42 * 10'


# To tokenize the string, you need to do more than merely match patterns.
# You need to have some way to identify the kind of pattern as well. For
# instance, you might want to turn the string into a sequence of pairs like
# this:


tokens = [('NAME', 'foo'), ('EQ', '='), ('NUM', '23'), ('PLUS', '+'),
          ('NUM', '42'), ('TIMES', '*'), ('NUM', '10')]


# To do this kind of splitting, the first step is to define all of the
# possible tokens, including whitespace, by regular expression patterns
# using named capture groups such as this:


import re
NAME = r'(?P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'
NUM = r'(?P<NUM>\d+)'
PLUS = r'(?P<PLUS>\+)'
TIMES = r'(?P<TIMES>\*)'
EQ = r'(?P<EQ>=)'
WS = r'(?P<WS>\S+)'

master_pat = re.compile('|'.join([NAME, NUM, PLUS, TIMES, EQ, WS]))


# In these re patterns, the ?P<TOKENNAME> convention is used to assign a
# name to the pattern. This will be used later.

# Next, to tokenize, use the little-known scanner() method of pattern
# objects. This method creates a scanner object in which repeated calls to
# match() step through the supplied text one match at a time. Here is an
# interactive example of how a scanner object works:


scanner = master_pat.scanner('foo = 42')

scanner.match()
# <_sre.SRE_Match object at 0x100677738>

_.lastgroup, _.group()
# ('NAME', 'foo')

scanner.match()
# <_sre.SRE_Match object at 0x100677738>

_.lastgroup, _.group()
# ('WS', ' ')

scanner.match()
# <_sre.SRE_Match object at 0x100677738>

_.lastgroup, _.group()
# ('EQ', '=')

scanner.match()
# <_sre.SRE_Match object at 0x100677738>

_.lastgroup, _.group()
# ('WS', ' ')

scanner.match()
# <_sre.SRE_Match object at 0x100677738>

_.lastgroup, _.group()
('NUM', '42')

scanner.match()


# To take this technique and put it into code, it can be cleaned up and
# easily packaged into a generator like this:


from collections import namedtuple

Token = namedtuple('Token', ['type', 'value'])

def generate_tokens(pat, text):
    scanner = pat.scanner(text)
    for m in iter(scanner.match, None):
        yield Token(m.lastgroup, m.group())

# Example use
for tok in generate_tokens(master_pat, 'foo = 42'):
    print(tok)

# Produces output
# Token(type='NAME', value='foo')
# Token(type='WS', value=' ')
# Token(type='EQ', value='=')
# Token(type='WS', value=' ')
# Token(type='NUM', value='42')


# If you want to filter the token stream in some way, you can either define
# more generator functions or use a generator expression. For example, here
# is how you might filter out all whitespace tokens.


tokens = (tok for tok in generate_tokens(master_pat, text)
            if tok.type != 'WS')

for tok in tokens:
    print(tok)


# Tokenizing is often the first step for more advanced kinds of text
# parsing and handling. To use the scanning technique shown, there are a
# few important details to keep in mind. First, you must make sure that you
# identify every possible text sequence that might appear in the input with
# a corresponding re pattern. If any nonmatching text is found, scanning
# simply stops. This is why it was necessary to specify the whitespace (WS)
# token in the example.

# The order of tokens in the master regular expression also matters. When
# matching, re tries to match patterns in the order specified. Thus, if a
# pattern happens to be a substring of a longer pattern, you need to make
# sure the longer pattern goes first.


# For example:


LT = r'(?P<LT><)'
LE = r'(?P<LE><=)'
EQ = r'(?P<EQ>=)'

master_pat = re.compile('|'.join([LE, LT, EQ]))         # Correct
# master_pat = re.compile('|'.join([LT, LE, EQ]))       # Incorrect


# The second pattern is wrong because it would match the text <= as the
# token LT followed by the token EQ, not the single token LE, as was
# probably desired.

# Last, but not least, you need to watch out for patterns that form
# substrings. For example, suppose you have two patterns like this:


PRINT = r'(P<PRINT>print)'
NAME = r'(P<NAME>[a-zA-Z_][a-zA-Z_0-9]*)'

master_pat = re.compile('|'.join([PRINT, NAME]))

for tok in generate_tokens(master_pat, 'printer'):
    print(tok)

# Outputs:
# Token(type='PRINT', value='print')
# Token(type='NAME', value='er')


# For more advanced kinds of tokenizing, you may want to check out packages
# such as PyParsing (http://pyparsing.wikispaces.com) or PLY
# (http://www.dabeaz.com/ply/index.html). An example involving PLY appears
# in '19)'.


# 19) Writing a Simple Recursive Descent Parser


# You need to parse text according to a set of grammar rules and perform
# actions or build an abstract syntax tree representing the input. The
# grammar is small, so you'd prefer to just write the parser yourself as
# opposed to using some kind of framework.

# In this problem, we're focused on the problem of parsing text according
# to a particular grammar. In order to do this, you should probably start
# by having a formal specification of the grammar in the form of a BNF or
# EBNF. For example, a grammar for simple arithmetic expressions might look
# like this:

expr ::= expr + term
    |   expr - term
    |   term

term ::= term * factor
    | term / factor
    | factor

factor ::= (expr)
    |   NUM


# Or alternatively, in EBNF form:

expr ::= term { (+|-) term }*

term ::= factor { (*|/) factor }*

factor ::= (expr)
        |   NUM


# In an EBNF, parts of a rule enclosed in { ... }* are optional. The *
# means zero or more repetitions (the same meaning as in a regular
# expression).

# Now, if you're not familiar with the mechanics of working with a BNF,
# think of it as a specification of substitution or replacement rules where
#  symbols on the left side can be replaced by the symbols on the right (or
# vice versa). Generally, what happens during parsing is that you try to
# match the input text to the grammar by making various substitutions and
# expansions using the BNF. To illustrate, suppose you are parsing an
# expression such as 3 + 4 * 5. This expression would first need to be
# broken down into a token stream, using the techniques described in "18)".
# The result might be a sequence of tokens like this:


NUM + NUM + NUM


# From there, parsing involves trying to match the grammar to input tokens
# by making substitutions:


expr
expr ::= term { (+|-) term }*
expr ::= factor { (*|/) factor }* { (+|-) term }*
expr ::= NUM { (*|/) factor}* { (+|-) term}*
expr ::= NUM { (+|-) term}*
expr ::= NUM + term { (+|-) term }*
expr ::= NUM + factor { (*|/) factor }* { (+|-) term }*
expr ::= NUM + NUM { (*|/) factor}* { (+|-) term }*
expr ::= NUM + NUM * factor { (*|/) factor}* { (+|-) term }*
expr ::= NUM + NUM + NUM { (*|/) factor}* { (+|-) term }*
expr ::= NUM + NUM + NUM { (+|-) term}*
expr ::= NUM + NUM + NUM


# Following all of the substitution steps takes a bit of coffee, but
# they're driven by looking at the input and trying to match it to grammar
# rules. The first input token is a NUM, so substitutions first focus on
# matching that part. Once matched, attention moves to the next token of +
# and so on. Certain parts of the righthand side (e.g., { (*/) factor }*)
# disappear when it's determined that they can't match the next token. In a
# successful parse, the entire righthand side is expanded completely to
# match the input token stream.

# With all of the preceding background in place, here is a simple example
# that shows how to build a recursive descent expression evaluator:


import re
import collections

# Token specification
NUM =    r'(?P<NUM>\d+)'
PLUS =   r'(?P<PLUS>\+)'
MINUS =  r'(?P<MINUS>-)'
TIMES =  r'(?P<TIMES>\*)'
DIVIDE = r'(?P<DIVIDE>/)'
LPAREN = r'(?P<LPAREN>\()'
RPAREN = r'(?P<RPAREN>\))'
WS =     r'(?P<WS>\S+)'

master_pat = re.compile('|'.join([NUM, PLUS, MINUS, TIMES
                                  DIVIDE, LPAREN, RPAREN, WS]))

# Tokenizer
Token = collections.namedtuple('Token', ['type', 'value'])

def generate_tokens(text):
    scanner = master_pat.scanner(text)
    for m in iter(scanner.match, None):
        tok = Token(m.lastgroup, m.group())
        if tok.type != 'WS':
            yield tok

# Parser
class ExpressionEvaluator:
    '''
    Implementation of a recursive descent parser. Each method implements a
    single grammar rule. Use the ._accept() method to test and accept the
    current lookahead token. Use the ._expect() method to exactly match and
    discard the next token on the input (or raise a SyntaxError if it
    doesn't match).
    '''

    def parse(self,text):
        self.tokens = generate_tokens(text)
        self.tok = None             # Last symbol consumed
        self.nexttok = None         # Next symbol tokenized
        self._advance()             # Load first lookahead token
        return self.expr()

    def _advance(self):
        'Advance one token ahead'
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        'Test and consume the next token if it matches toktype'
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        'Consume next token if it matches toktype or raise SyntaxError'
        if not self._accept(toktype)
            raise SyntaxError('Expected ' + toktype)

    # Grammar rules follow

    def expr(self):
        "expression ::= term { ('+'|'-') term )*"

        exprval = self.term()
        while self._accept('PLUS') or self._accept('MINUS'):
            op = self.tok.type
            right = self.term()
            if op == 'PLUS':
                exprval += right
            elif op == 'MINUS':
                exprval -= right
            return exprval

    def term(self):
        "term ::= factor { ('*'|'/') factor }*"

        termval = self.factor()
        while self._accept('TIMES') or self._accept('DIVIDE'):
            op = self.tok.type
            right = self.factor()
            if op == 'TIMES':
                termval *= right
            elif op == 'DIVIDE':
                termval /= right
        return termval

    def factor(self):
        "factor ::= NUM | (expr)"

        if self._accept('NUM'):
            return int(self.tok.value)
        elif self._accept('LPAREN'):
            exprval = self.expr()
            self._expect('RPAREN')
            return exprval
        else:
            raise SyntaxError('Expected NUMBER or LPAREN')


# Here is an example of using the ExpressionEvaluator class interactively:


e = ExpressionEvaluator()

e.parse('2')
# 2

e.parse('2 + 3')
# 5

e.parse('2 + 3 * 4')
# 14

e.parse('2 + (3 + 4) * 5')
# 37

e.parse('2 + (3 + * 4)')
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
#   File "exprparse.py", line 40, in parse
#       return self.expr()
#   File "exprparse.py", line 67, in expr
#       right = self.term()
#   File "exprparse.py", line 77 in term
#       termval = self.factor()
#   File "exprparse.py", line 93, in factor
#       exprval = self.expr()
#   File "exprparse.py", line 67, in expr
#       right = self.term()
#   File "exprparse.py", line 77, in term
#       termval = self.factor()
#   File "exprparse.py", line 97, in factor
#       raise SyntaxError("Expected NUMBER or LPAREN")
# SyntaxError: Expected NUMBER or LPAREN


# If you want to do something other than pure evaluation, you need to
# change the ExpresionEvaluator class to do something else. For example,
# here is an alternative implementation that constructs a simple parse
# tree:

class ExpressionTreeBuilder(ExpressionEvaluator):
    def expr(self):
        "expression :: = term { ('+'|'-') term }"

        exprval = self.term()
