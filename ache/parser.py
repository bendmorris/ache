from pyparsing import *


class Variable:
    def __init__(self, name, default=None):
        self.name = name
        self.default = default

    def bind(self, value, context):
        context[self.name] = value

    def eval(self, context=None):
        return context.get(self.name, self.default.eval(context) if not self.default is None else None)

    def __str__(self):
        if self.default is None:
            return '$%s' % self.name
        else:
            return '$%s | %s' % (self.name, self.default)
    def __repr__(self): return str(self)


class Literal:
    def __init__(self, expr):
        self.expr = expr

    def bind(self, value, context):
        pass

    def eval(self, context=None):
        print self.expr
        return eval(self.expr)

    def __str__(self): return '`%s`' % self.expr
    def __repr__(self): return str(self)


expr = Forward()

identifier = Suppress("$") + Word(alphanums)
identifier.setParseAction(lambda x: Variable(*x))

defaultValue = identifier + Suppress("|") + expr
defaultValue.setParseAction(lambda x: Variable(x[0].name, x[1]))

literal = QuotedString(quoteChar='`')
literal.setParseAction(lambda x: Literal(*x))

expr << (
    (Suppress("(") + expr + Suppress(")")) |
    (defaultValue | identifier | literal)
)

def parse(e):
    return expr.parseString(e, parseAll=True)[0]
