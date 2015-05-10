from collections import defaultdict
from itertools import chain
from parser import parse



__version__ = '0.1.0'

class Rule(object):
    builtin = False

    @classmethod
    def parse(cls, node, builtin_rules):
        """Generate a rule from an ElementTree node."""

        if node.tag in builtin_rules:
            r = builtin_rules[node.tag](node)
        else:
            r = Rule(node.tag)

        for key, val in node.attrib.iteritems():
            r.attributes[key] = parse(val)

        for child in node:
            child_rule = Rule.parse(child, builtin_rules)
            child_rule.parent = r
            r.children.append(child_rule)

        return r

    def __init__(self, name):
        self.name = name
        self.children = []
        self.attributes = {}
        self.required = set()
        self.parent = None

    def attr(self, a, context):
        """Evaluate a variable in the given context."""
        if a in self.attributes:
            return self.attributes[a].eval(context)
        elif self.parent is not None:
            return self.parent.attr(a, context)
        else:
            return None

    def match(self, node):
        """Returns True if this rule matches the given node."""
        return self.builtin or all(attr in node.iter for attr in self.required)

    def execute(self, node, context, rules):
        # bind attribute values
        for key, val in node.attrib.iteritems():
            if key in self.attributes:
                self.attributes[key].bind(val, context)

        return self.execute_children(node, context, rules)

    def execute_children(self, node, context, rules):
        # evaluate child nodes
        remaining = list(node)

        result = False

        for rule in self.children:
            if rule.builtin:
                # builtin nodes match against the current node
                if rule.match(node):
                    context = {k:v for (k,v) in context.iteritems()}
                    # bind attributes
                    if rule.execute(node, context, rules):
                        result = True

            else:
                # other nodes try to match against child nodes
                for child in remaining:
                    if rule.match(child):
                        context = {k:v for (k,v) in context.iteritems()}
                        # bind attributes
                        if rule.execute(child, context, rules):
                            result = True
                        remaining.remove(child)

        return result


    def __str__(self): return self.to_string()
    def __repr__(self): return str(self)

    def to_string(self, indent=0):
        return '\n'.join([('  ' * indent) + self.name] + [rule.to_string(indent+1) for rule in self.children])
