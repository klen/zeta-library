from pyparsing import SkipTo, Optional, Literal, cStyleComment, dblSlashComment


COMMENT = cStyleComment | dblSlashComment
REQUIRE = Literal("require(") + SkipTo(")")("path") + Literal(")") + Optional(Literal(";"))
