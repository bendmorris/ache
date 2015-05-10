import os
import glob
import imp
import inspect
from collections import defaultdict
from ache import Rule

builtin_rules = defaultdict(lambda: None)

mods = [
    script
    for script in glob.glob(os.path.join(os.path.dirname(__file__), '*.py'))
    if not os.path.basename(script).startswith('_')
]

for filename in mods:
    modname = os.path.basename(filename)[:-len('.py')]
    mod = imp.load_source(modname, filename)
    vars = dir(mod)
    for var in vars:
        cls = getattr(mod, var)
        if inspect.isclass(cls) and issubclass(cls, Rule) and not cls is Rule:
            cls.builtin = True
            builtin_rules[cls.name] = cls
