from collections import defaultdict
import xml.etree.cElementTree as ET
from __init__ import Rule
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
                rules[rule.tag].append(Rule.parse(rule, builtin_rules))

        else:
            # execute the first matching rule definition, if any
            if child.tag in rules:
                for rule in rules[child.tag]:
                    if rule.match(child):
                        context = {}
                        matches += 1
                        if rule.execute(child, context, rules):
                            executions += 1
                        break

    print "*** Finished ***\n- Evaluated %s rules.\n- Found %s matching assets.\n- Executed %s actions." % (len(rules), matches, executions)


def run():
    import argparse

    parser = argparse.ArgumentParser(description='Ache: make for asset pipelines.')
    parser.add_argument('files', nargs='+', help='pipeline XML files to process')
    args = parser.parse_args()

    for filename in args.files:
        with open(filename) as input_file:
            process_file(input_file)


if __name__ == '__main__':
    run()
