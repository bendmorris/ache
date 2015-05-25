from collections import defaultdict
import xml.etree.cElementTree as ET
from __init__ import Rule, args
from rules import builtin_rules


def process_file(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    rules = defaultdict(list, {})

    matches = 0
    executions = 0
    for child in root:
        if child.tag == 'rules':
            # define new rules
            for rule in child:
                try:
                    parsed = Rule.parse(rule, builtin_rules)
                except Exception as e:
                    print ET.tostring(rule)
                    raise e
                rules[rule.tag].append(parsed)

        else:
            # execute the first matching rule definition, if any
            if child.tag in rules:
                matched = False
                for rule in rules[child.tag]:
                    if rule.match(child):
                        if args.verbose:
                            print '\n** Rule matched:', rule
                            print ET.tostring(child)
                        context = {}
                        matches += 1
                        if rule.execute(child, context, rules):
                            executions += 1
                        matched = True
                        break

                if not matched:
                    print '\n*** NO MATCH FOUND: ', ET.tostring(child)

    print "*** Finished ***\n- Evaluated %s rules.\n- Found %s matching assets.\n- Executed %s actions." % (len(rules), matches, executions)


def run():
    import argparse

    for filename in args.files:
        with open(filename) as input_file:
            process_file(input_file)


if __name__ == '__main__':
    run()
