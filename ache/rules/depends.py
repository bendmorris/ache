import os
from ache import Rule, args


class Depends(Rule):
    """Only evaluate the following expressions if the source has been modified
    more recently than the target, or the target doesn't exist."""

    name = 'depends'

    def __init__(self, node):
        Rule.__init__(self, self.name)

    def execute(self, node, context, rules):
        source_file = self.attributes['source'].eval(context)
        target_file = self.attributes['target'].eval(context)

        if not os.path.exists(source_file):
            if args.verbose:
                print 'Source %s not found' % source_file
            return

        source_mtime = os.path.getmtime(source_file)
        target_mtime = os.path.getmtime(target_file) if os.path.exists(target_file) else 0

        if target_mtime < source_mtime:
            if args.verbose:
                print 'Target %s being generated from source %s' % (target_file, source_file)
            return self.execute_children(node, context, rules)

        if args.verbose:
            print 'Target %s newer than source %s' % (target_file, source_file)

        return False
