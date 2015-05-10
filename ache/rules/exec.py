import os
import re
import subprocess
from ache import Rule


variable = re.compile("\$[A-Za-z0-9]+")

class Exec(Rule):
    """Execute one or more shell commands."""

    name = 'exec'

    def __init__(self, node):
        Rule.__init__(self, self.name)
        self.expr = '\n'.join(line.strip() for line in node.text.split('\n') if line.strip())

    def execute(self, node, context, rules):
        expr = self.format_expr(context)
        print expr
        subprocess.call(expr, shell=True)
        return True

    def format_expr(self, context):
        expr = self.expr
        vars = set(variable.findall(expr))
        for var in vars:
            varname = var.lstrip('$')
            expr = expr.replace(
                var,
                context[varname] if varname in context else self.attr(var.lstrip('$'), context)
            )

        return expr
