from pyparsing import Suppress, SkipTo, Optional, SkipTo, Literal


LINE_COMMENT = Suppress("//") + SkipTo("\n")
REQUIRE = Literal("require(") + SkipTo(")")("path") + Literal(")") + Optional(Literal(";"))
