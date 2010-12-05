from pyparsing import Word, Suppress, Literal, alphanums, alphas, hexnums, nums, SkipTo, oneOf, ZeroOrMore, Optional, Group, OneOrMore, Forward

VAR_CONTEXT = dict()
MIXIN_CONTEXT = dict()

IDENT = Word(alphas + "_", alphanums + "_-")
NAME = Word(alphanums + "_-")
NUMBER = Word(nums + '.-')
COMMA, COLON, SEMICOLON, LACC, RACC, LPAREN, RPAREN, LBRACK, RBRACK = map(Suppress, ",:;{}()[]")
QUOTES = oneOf('" \'').suppress()

COMMENT_BEGIN = "/*"
COMMENT_END = "*/"
COMMENT = COMMENT_BEGIN + SkipTo(COMMENT_END) + COMMENT_END

CDO = Literal("<!--")
CDC = Literal("-->")
INCLUDES = "~="
DASHMATCH = "|="
IMPORT_SYM = Literal("@import")
PAGE_SYM = Literal("@page")
MEDIA_SYM = Literal("@media")
FONT_FACE_SYM = Literal("@font-face")
CHARSET_SYM = Literal("@charset")
SASS_MIXIN_SYM = Suppress("@mixin")
SASS_INCLUDE_SYM = Suppress("@include")

IMPORTANT_SYM = Literal("!") + Literal("important")

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

OPERATOR = oneOf("/ ,")
SASS_OPERATOR = oneOf("+ - / *")
COMBINATOR = oneOf("+ >")
UNARY_OPERATOR = oneOf("- +")

ELEMENT_NAME = IDENT | Literal("*")
CLASS = Word('.', alphanums + "-_")
ATTRIB = LBRACK + SkipTo("]") + RBRACK
PSEUDO = Word(':', alphanums + "-_") | (COLON + FUNCTION + IDENT + RPAREN)

SELECTOR_FILTER = HASH | CLASS | ATTRIB | PSEUDO
SELECTOR = (ELEMENT_NAME + SELECTOR_FILTER) | ELEMENT_NAME | SELECTOR_FILTER
SELECTOR_TREE = Group(OneOrMore(Optional(COMBINATOR) + SELECTOR))
SELECTOR_GROUP = Group(SELECTOR_TREE + ZeroOrMore(COMMA + SELECTOR_TREE))

PRIO = IMPORTANT_SYM.suppress()

SASS_VAR = Suppress("$") + IDENT
def sassvar_parse( s, l, t ):
    return VAR_CONTEXT.get(t[0], '')
SASS_VAR.setParseAction(sassvar_parse)

TERM = Group(Optional(UNARY_OPERATOR) + (( LENGTH | PERCENTAGE
            | FREQ | EMS | EXS | ANGLE | TIME | NUMBER
        ) | IDENT | URI | HEXCOLOR | (SASS_VAR + Optional(SASS_OPERATOR + NUMBER))))

EXPR = TERM + ZeroOrMore(Optional(OPERATOR) + TERM)
def parse_expr(s, l, t):
    values = []
    for ex in t:
        if len(ex) < 4:
            return
        try:
            value = str(eval(ex[0] + ''.join(ex[2:])))
        except SyntaxError:
            continue
        values.append(value + ex[1])
    return ' '.join(values)
EXPR.setParseAction(parse_expr)

DECLARATION = Group(NAME + COLON + EXPR + Optional(PRIO))

SASS_INCLUDE = Group(SASS_INCLUDE_SYM + IDENT("name") + Optional(LPAREN + EXPR + RPAREN)("value") + SEMICOLON)

SASS_VAR_ASSIGMENT = Suppress("$") + IDENT + COLON + EXPR + Optional(PRIO) + SEMICOLON
def sass_var_assigment_parse( s, l, t ):
    name, value = t
    if not VAR_CONTEXT.has_key(name):
        VAR_CONTEXT[name] = list(value)
    return ''
SASS_VAR_ASSIGMENT.setParseAction(sass_var_assigment_parse)

RULESET = Forward()
RULESET << ( SELECTOR_GROUP("selectors") + LACC + ZeroOrMore(DECLARATION + Optional(SEMICOLON))("declarations") + ZeroOrMore(SASS_INCLUDE)("includes") + ZeroOrMore(RULESET)("rulesets") + RACC )
def ruleset_parse(s, l, t):
    head = __render_selectors(t.selectors)
    body = __render_declarations(t.declarations) + __render_declaration_includes(t.includes)
    out = ''
    if body:
        out += head + '{' + body + '}\n\n'
    return out + __render_ruleset_includes(head, t.includes) + __render_rulesets(head, t.rulesets)
RULESET.setParseAction(ruleset_parse)
RULESET.ignore(COMMENT)

SASS_MIXIN = SASS_MIXIN_SYM + IDENT + Optional(LPAREN + Suppress("$") + IDENT("var") + RPAREN) + LACC + ZeroOrMore(DECLARATION + Optional(SEMICOLON))("declarations") + ZeroOrMore(RULESET)("rulesets") + RACC
def parse_mixin(s, l, t):
    name = t[0]
    if not MIXIN_CONTEXT.has_key(name):
        MIXIN_CONTEXT[name] = {
            'var': t.var,
            'declarations': t.declarations,
            'rulesets': t.rulesets }
    return ''
SASS_MIXIN.setParseAction(parse_mixin)

IMPORT = IMPORT_SYM + URI + Optional(IDENT + ZeroOrMore(IDENT)) + SEMICOLON
MEDIA = MEDIA_SYM + IDENT + ZeroOrMore(COMMA + IDENT) + LACC + ZeroOrMore( RULESET | SASS_MIXIN ) + RACC
MEDIA.ignore(COMMENT)
FONT_FACE = FONT_FACE_SYM + LACC + DECLARATION + ZeroOrMore(SEMICOLON + DECLARATION) + RACC
PSEUDO_PAGE = ":" + IDENT
PAGE = PAGE_SYM + Optional(IDENT) + Optional(PSEUDO_PAGE) + LACC + DECLARATION + ZeroOrMore(SEMICOLON + DECLARATION) + RACC

STYLESHEET = (
        Optional( CHARSET_SYM + IDENT + SEMICOLON ) +
        ZeroOrMore(CDC | CDO) +
        ZeroOrMore(IMPORT + Optional(ZeroOrMore(CDC | CDO))) +
        ZeroOrMore(
            ( SASS_VAR_ASSIGMENT | RULESET | MEDIA | PAGE | FONT_FACE | SASS_MIXIN ) +
            ZeroOrMore(CDC | CDO)
        )
)

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
