from pyparsing import Word, Suppress, Literal, alphanums, alphas, hexnums, nums, SkipTo, oneOf, ZeroOrMore, Optional, Group, OneOrMore, Forward, cStyleComment


# Mixin and variables context
GLOBAL_CONTEXT = dict()
LOCAL_CONTEXT = dict()
MIXIN_CONTEXT = dict()

# Base css word and literals
IDENT = Word(alphas + "_", alphanums + "_-")
NAME = Word(alphanums + "_-")
NUMBER = Word(nums + '.-')
COMMA, COLON, SEMICOLON = [Suppress(c) for c in ",:;"]
LACC, RACC, LPAREN, RPAREN, LBRACK, RBRACK = [Suppress(c) for c in "{}()[]"]

# Comment
COMMENT = cStyleComment

# Directives
CDO = Literal("<!--")
CDC = Literal("-->")
INCLUDES = "~="
DASHMATCH = "|="
IMPORTANT_SYM = Literal("!") + Literal("important")
IMPORT_SYM = Literal("@import")
PAGE_SYM = Literal("@page")
MEDIA_SYM = Literal("@media")
FONT_FACE_SYM = Literal("@font-face")
CHARSET_SYM = Literal("@charset")
MIXIN_SYM = Suppress("@mixin")
INCLUDE_SYM = Suppress("@include")

# Property values
HASH = Word('#', alphanums + "_-")
HEXCOLOR = Literal("#") + Word(hexnums, min=3, max=6)
EMS = NUMBER + Literal("em")
EXS = NUMBER + Literal("ex")
LENGTH = NUMBER + oneOf("px cm mm in pt pc")
ANGLE = NUMBER + oneOf("deg rad grad")
TIME = NUMBER + oneOf("ms s")
FREQ = NUMBER + oneOf("Hz kHz")
DIMEN = NUMBER + IDENT
PERCENTAGE = NUMBER + Literal("%")
URI = Literal("url(") + SkipTo(")")("path") + Literal(")")
FUNCTION = IDENT + Literal("(")
PRIO = IMPORTANT_SYM.suppress()

# Operators
OPERATOR = oneOf("/ ,")
MATH_OPERATOR = oneOf("+ - / *")
COMBINATOR = oneOf("+ >")
UNARY_OPERATOR = oneOf("- +")

# Simple selectors
ELEMENT_NAME = IDENT | Literal("*")
CLASS = Word('.', alphanums + "-_")
ATTRIB = LBRACK + SkipTo("]") + RBRACK
PSEUDO = Word(':', alphanums + "-_") | (COLON + FUNCTION + IDENT + RPAREN)

# Selectors
SELECTOR_FILTER = HASH | CLASS | ATTRIB | PSEUDO
SELECTOR = (ELEMENT_NAME + SELECTOR_FILTER) | ELEMENT_NAME | SELECTOR_FILTER
SELECTOR_TREE = Group(OneOrMore(Optional(COMBINATOR) + SELECTOR))
SELECTOR_GROUP = Group(SELECTOR_TREE + ZeroOrMore(COMMA + SELECTOR_TREE))

# Variables
VARIABLE = Suppress("$") + IDENT
VAR_STRING = VARIABLE + ZeroOrMore(MATH_OPERATOR + NUMBER)
def parse_variables(s, l, t):
    value, units = LOCAL_CONTEXT.get(t[0]) or GLOBAL_CONTEXT.get(t[0], ('$'+t[0],''))
    if len(t) > 1:
        try:
            value = str(eval(value + ''.join(t[1:])))
        except SyntaxError:
            return
    return value + units
VAR_STRING.setParseAction(parse_variables)

# Property values
TERM = Group(Optional(UNARY_OPERATOR) + (( LENGTH | PERCENTAGE
            | FREQ | EMS | EXS | ANGLE | TIME | NUMBER
        ) | IDENT | URI | HEXCOLOR | VAR_STRING))
EXPR = TERM + ZeroOrMore(Optional(OPERATOR) + TERM)
DECLARATION = Group(NAME + COLON + EXPR + Optional(PRIO))
# def parse_declarations(s, l, t):
    # return ''
# DECLARATION.setParseAction(parse_declarations)

# Include
INCLUDE_PARAMS = LPAREN + EXPR + RPAREN
INCLUDE = Group(INCLUDE_SYM + IDENT("name") + Optional(INCLUDE_PARAMS)("params") + SEMICOLON)

# Global variable assigment
VARIABLE_ASSIGMENT = Suppress("$") + IDENT + COLON + EXPR + Optional(PRIO) + SEMICOLON
def parse_variable_assigment( s, l, t ):
    name, value = t
    if not GLOBAL_CONTEXT.has_key(name):
        GLOBAL_CONTEXT[name] = list(value)
    return ''
VARIABLE_ASSIGMENT.setParseAction(parse_variable_assigment)

# Ruleset
RULESET = Forward()
RULESET << (
        SELECTOR_GROUP("selectors") +
        LACC +
        ZeroOrMore(DECLARATION + Optional(SEMICOLON))("declarations") +
        ZeroOrMore(INCLUDE)("includes") +
        ZeroOrMore(RULESET)("rulesets") +
        RACC )
def parse_ruleset(s, l, t):
    head = __render_selectors(t.selectors)
    body = __render_declarations(t.declarations) + __render_declaration_includes(t.includes)
    out = ''
    if body:
        out += head + '{' + body + '}\n\n'
    return out + __render_ruleset_includes(head, t.includes) + __render_rulesets(head, t.rulesets)
RULESET.setParseAction(parse_ruleset)

# Mixins
MIXIN_PARAMS = LPAREN + VARIABLE + RPAREN
def parse_mixin_params(s, l, t):
    LOCAL_CONTEXT[t[0]] = ("&", t[0])
MIXIN_PARAMS.setParseAction(parse_mixin_params)
MIXIN = ( MIXIN_SYM + IDENT +
    Optional(MIXIN_PARAMS) +
    LACC +
    ZeroOrMore(DECLARATION + Optional(SEMICOLON))("declarations") +
    ZeroOrMore(RULESET)("rulesets") +
    RACC )
def parse_mixin(s, l, t):
    name = t[0]
    if not MIXIN_CONTEXT.has_key(name):
        MIXIN_CONTEXT[name] = {
            'declarations': t.declarations,
            'rulesets': t.rulesets }
    print MIXIN_CONTEXT
    return ''
MIXIN.setParseAction(parse_mixin)

IMPORT = IMPORT_SYM + URI + Optional(IDENT + ZeroOrMore(IDENT)) + SEMICOLON
MEDIA = MEDIA_SYM + IDENT + ZeroOrMore(COMMA + IDENT) + LACC + ZeroOrMore( RULESET | MIXIN ) + RACC
FONT_FACE = FONT_FACE_SYM + LACC + DECLARATION + ZeroOrMore(SEMICOLON + DECLARATION) + RACC
PSEUDO_PAGE = ":" + IDENT
PAGE = PAGE_SYM + Optional(IDENT) + Optional(PSEUDO_PAGE) + LACC + DECLARATION + ZeroOrMore(SEMICOLON + DECLARATION) + RACC

STYLESHEET = (
        Optional( CHARSET_SYM + IDENT + SEMICOLON ) +
        ZeroOrMore(CDC | CDO) +
        ZeroOrMore(IMPORT + Optional(ZeroOrMore(CDC | CDO))) +
        ZeroOrMore(
            ( VARIABLE_ASSIGMENT | MIXIN | RULESET | MEDIA | PAGE | FONT_FACE ) +
            ZeroOrMore(CDC | CDO)
        )
).ignore(COMMENT)


def __render_selectors( selector_group ):
    selectors = []
    for sel_tree in selector_group:
        selectors.append(' '.join(sel for sel in sel_tree))
    return ', '.join(selectors) + ' '


def __render_declarations( declarations ):
    out = sym = ''
    if len(declarations) > 1:
        sym = '\n\t'
    for declare in declarations:
        name = declare[0]
        out += sym + name + ':'
        vals = declare[1:]
        for value in vals:
            out += ' ' + ''.join(value)
        out += ';'
    return out.strip(';')


def __render_declaration_includes( includes ):
    out = ''
    for include in includes:
        if MIXIN_CONTEXT.has_key(include.name):
            for declare in MIXIN_CONTEXT[include.name]['declarations']:
                name, value = declare
                out += '\n\t' + name + ':' + ''.join(value) + ';'
    return out


def __render_ruleset_includes( head, includes ):
    out = ''
    for include in includes:
        if MIXIN_CONTEXT.has_key(include.name):
            for rules in MIXIN_CONTEXT[include.name]['rulesets']:
                out += head + ' ' + rules
    return out


def __render_rulesets( head, rulesets ):
    out = ''
    for ruleset in rulesets:
        out += head + ruleset
    return out

if __name__ == '__main__':
    print STYLESHEET.transformString("""

$blue: #3bbfce;
$margin: 16px;

.content-navigation {
  border-color: $blue;
  color: $blue;
  border-bottom: $green;
}

@mixin left($dist) {
  float: left;
  margin-left: $dist;
}

.border {
  padding: $margin / 2;
  margin: $margin / 2 $margin + 6;
  border-color: $blue;
}

@mixin table-base {
  th {
    text-align: center;
    font-weight: bold;
  }
  /* test comment */
  td, th {padding: 2px}
}

#data {
  @include left(10px);
  @include table-base;
}
    """)
