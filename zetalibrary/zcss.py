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
PRIO = IMPORTANT_SYM

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
SELECTOR = Group(ELEMENT_NAME + SELECTOR_FILTER) | ELEMENT_NAME | SELECTOR_FILTER
SELECTOR_TREE = Group(OneOrMore(Optional(COMBINATOR) + SELECTOR))
SELECTOR_GROUP = SELECTOR_TREE + ZeroOrMore(COMMA + SELECTOR_TREE)
def parse_selector_group(s, l, t):
    selectors = []
    for sel_tree in t:
        selectors.append(' '.join(''.join(sel) for sel in sel_tree))
    return ', '.join(selectors) + ' '
SELECTOR_GROUP.setParseAction(parse_selector_group)

# Variables
VAR_SYM = "$"
LOCALVAR_SYM = "@"
VARIABLE = Suppress(VAR_SYM) + IDENT
LOCAL_VARIABLE = Suppress(LOCALVAR_SYM) + IDENT
VAR_STRING = VARIABLE + ZeroOrMore(MATH_OPERATOR + NUMBER)
LOCVAR_STRING = LOCAL_VARIABLE + ZeroOrMore(MATH_OPERATOR + NUMBER)
def parse_variables(s, l, t):
    value, units = LOCAL_CONTEXT.get(t[0]) or GLOBAL_CONTEXT.get(t[0], ('$'+t[0],''))
    if value == LOCALVAR_SYM:
        return value + units + ' '.join(t[1:])
    elif len(t) > 1:
        try:
            value = str(eval(value + ''.join(t[1:])))
        except SyntaxError:
            return
    return value + units
VAR_STRING.setParseAction(parse_variables)
LOCVAR_STRING.setParseAction(parse_variables)

# Property values
TERM = Group(Optional(UNARY_OPERATOR) + (( LENGTH | PERCENTAGE
            | FREQ | EMS | EXS | ANGLE | TIME | NUMBER
        ) | IDENT | URI | HEXCOLOR | VAR_STRING))
EXPR = TERM + ZeroOrMore(Optional(OPERATOR) + TERM)
FUNC_EXPR = OneOrMore(TERM)
DECLARATION = Group(NAME + COLON + EXPR + Optional(PRIO) + Optional(SEMICOLON))("declaration")

# Declare group
DECLARE_SELECTOR = IDENT + COLON
DECLARESET = Forward()
DECLARESET << Group(DECLARE_SELECTOR + LACC + OneOrMore(DECLARESET | DECLARATION) + RACC)("declareset")

# Include
INCLUDE_PARAMS = LPAREN + FUNC_EXPR + ZeroOrMore(COMMA + FUNC_EXPR) + RPAREN
INCLUDE = Group(INCLUDE_SYM + IDENT("name") + Optional(INCLUDE_PARAMS("params")) + SEMICOLON)("include")
def parse_include(s, l, t):
    group = t[0]
    mixin = MIXIN_CONTEXT.get(group.name)
    if mixin and group.params:
        count = 0
        for var in mixin['vars']:
            try:
                value = __parse_value(group.params[count])
            except IndexError:
                value = GLOBAL_CONTEXT.get(var, ("$", var))
            LOCAL_CONTEXT[var[0]] = value
            count += 1
INCLUDE.setParseAction(parse_include)

# Global variable assigment
VARIABLE_ASSIGMENT = Suppress("$") + IDENT + COLON + EXPR + Optional(PRIO) + SEMICOLON
def parse_variable_assigment(s, l, t):
    name, value = t
    if not GLOBAL_CONTEXT.has_key(name):
        GLOBAL_CONTEXT[name] = __parse_value(value)
    return ''
VARIABLE_ASSIGMENT.setParseAction(parse_variable_assigment)

# Ruleset
RULESET = Forward()
RULESET << (
        SELECTOR_GROUP("selectors") +
        LACC + ZeroOrMore(VARIABLE_ASSIGMENT | DECLARESET | DECLARATION | INCLUDE | RULESET) + RACC )
def parse_ruleset(s, l, t):
    dec, rul = __parse_includes(t[1:])
    out = ''

    if dec:
        out += t.selectors + '{' + __render_declarations(dec) + '}\n\n'

    for ruleset in rul:
        out += '\n\n'.join( [t.selectors + ruls for ruls in ruleset.split('\n\n') if ruls] ) + '\n\n'
    return out
RULESET.setParseAction(parse_ruleset)

# Mixins
MIXIN_PARAM = Group(VARIABLE + Optional(COLON + FUNC_EXPR))
MIXIN_PARAMS = LPAREN + MIXIN_PARAM + ZeroOrMore(COMMA + MIXIN_PARAM) + RPAREN
def parse_mixin_params(s, l, t):
    for group in t:
        name = group[0]
        value = __parse_value(group[1]) if len(group) > 1 else (LOCALVAR_SYM, name)
        LOCAL_CONTEXT[name] = value
MIXIN_PARAMS.setParseAction(parse_mixin_params)

MIXIN = (MIXIN_SYM + IDENT + Optional(MIXIN_PARAMS)("params") +
    LACC + ZeroOrMore(VARIABLE_ASSIGMENT | DECLARATION | INCLUDE | RULESET)("content") + RACC)
def parse_mixin(s, l, t):
    name = t[0]
    if not MIXIN_CONTEXT.has_key(name):
        dec, rul = __parse_includes(t.content)
        MIXIN_CONTEXT[name] = {
            'declarations': dec,
            'rulesets': rul }
        if t.params:
            MIXIN_CONTEXT[name]['vars'] = t.params
    return ''
MIXIN.setParseAction(parse_mixin)

# Root elements
IMPORT = IMPORT_SYM + URI + Optional(IDENT + ZeroOrMore(IDENT)) + SEMICOLON
MEDIA = MEDIA_SYM + IDENT + ZeroOrMore(COMMA + IDENT) + LACC + ZeroOrMore( RULESET | MIXIN ) + RACC
FONT_FACE = FONT_FACE_SYM + LACC + DECLARATION + ZeroOrMore(SEMICOLON + DECLARATION) + RACC
PSEUDO_PAGE = ":" + IDENT
PAGE = PAGE_SYM + Optional(IDENT) + Optional(PSEUDO_PAGE) + LACC + DECLARATION + ZeroOrMore(SEMICOLON + DECLARATION) + RACC

# Css stylesheet
STYLESHEET = (
        Optional( CHARSET_SYM + IDENT + SEMICOLON ) +
        ZeroOrMore(CDC | CDO) +
        ZeroOrMore(IMPORT + Optional(ZeroOrMore(CDC | CDO))) +
        ZeroOrMore(
            ( VARIABLE_ASSIGMENT | MIXIN | RULESET | MEDIA | PAGE | FONT_FACE ) +
            ZeroOrMore(CDC | CDO)
        )
).ignore(COMMENT)


def __render_declarations( declarations, prefix="" ):
    sym = '' if len(declarations) == 1 else '\n\t'
    dec = set()
    for declare in declarations:
        d = sym + prefix + declare[0] + ":"
        value = declare[1:]
        for v in value:
            d += " " + "".join(v)
        dec.add(d)
    out = ';'.join(dec)
    return LOCVAR_STRING.transformString(out)


def __parse_includes( pr ):
    dec, decset, rul, inc = [], [], [], []
    for elem in pr:
        if isinstance(elem, str):
            rul.append(elem)
        elif elem.getName() == 'declareset':
            decset.append(elem)
        elif elem.getName() == 'declaration':
            dec.append(elem)
        elif elem.getName() == 'include':
            inc.append(elem)

    for include in inc:
        mixin = MIXIN_CONTEXT.get(include.name)
        if not mixin:
            continue
        dec += [d for d in mixin['declarations']]
        rul += [r for r in mixin['rulesets']]

    for decs in decset:
        dec += __get_declares(decs)

    return dec, rul


def __get_declares( declareset ):
    decs = []
    name = declareset[0]
    for dec in declareset[1:]:
        if dec.getName() == "declaration":
            decs.append([ name + "-" + dec[0], dec[1] ])
        elif dec.getName() == "declareset":
            declares = __get_declares(dec)
            for dd in declares:
                decs.append([ name + "-" + dd[0], dd[1] ])
    return decs


def __parse_value( parser_results ):
    value = list(parser_results)
    if len(value) == 1:
        value.append('')
    return value


def parse( src ):
    return STYLESHEET.transformString(src)


if __name__ == '__main__':
    print parse("""
$main-color: #ce4dd6;
$style: solid;

#navbar {
  border-bottom: {
    color: $main-color;
    style: $style;
  }
  th {
    color: red;
  }
}

""")
