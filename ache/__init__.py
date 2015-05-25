from collections import defaultdict
from itertools import chain
import argparse
from parser import parse


__version__ = '0.1.0'

parser = argparse.ArgumentParser(description='Ache: make for asset pipelines.')
parser.add_argument('files', nargs='*', default=['ache.xml'], help='pipeline XML files to process (defaults to local ache.xml)')
parser.add_argument('--verbose', '-v', action='store_true', default=False, help='extra output for debugging')
parser.add_argument('--test', '-t', action='store_true', default=False, help="display but don't execute <exec> tags")
args = parser.parse_args()

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
            try:
                r.attributes[key] = parse(val)
            except Exception as e:
                print val
                raise e

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

    def all_attributes(self, seen=None):
        if seen is None:
            seen = set()

        for a in self.attributes:
            if not a in seen:
                yield a
            seen.add(a)

        if not self.parent is None:
            for a in self.parent.all_attributes(seen):
                yield a

    def attr(self, a, context):
        """Evaluate a variable in the given context."""
        return context.get(a, None)

    def match(self, node):
        """Returns True if this rule matches the given node."""
        return self.builtin or all(attr in node.iter for attr in self.required)

    def execute(self, node, context, rules):
        # bind attribute values
        for key in self.attributes:
            a = self.attributes[key]
            if key in node.attrib:
                self.attributes[key].bind(node.attrib[key], context)

        # bind default values for missing attributes
        for key in self.attributes:
            if not key in node.attrib:
                self.attributes[key].bind_default(context)

        return self.execute_children(node, context, rules)

    def execute_children(self, node, context, rules):
        # evaluate child nodes
        remaining = list(node)
        base_context = context

        result = False

        for rule in self.children:
            if rule.builtin:
                # builtin nodes match against the current node
                if rule.match(node):
                    context = {k:v for (k,v) in base_context.iteritems()}
                    # bind attributes
                    if rule.execute(node, context, rules):
                        result = True

            else:
                # other nodes try to match against child nodes
                to_remove = set()
                for child in remaining:
                    if rule.match(child):
                        context = {k:v for (k,v) in base_context.iteritems()}
                        # bind attributes
                        if rule.execute(child, context, rules):
                            result = True
                        to_remove.add(child)
                for r in to_remove:
                    remaining.remove(r)

        return result


    def __str__(self): return self.to_string()
    def __repr__(self): return str(self)

    def to_string(self, indent=0):
        return '\n'.join([('  ' * indent) + self.name] + [rule.to_string(indent+1) for rule in self.children])
