from setuptools import setup
from ache.__init__ import __version__


setup(name='ache',
      version=__version__,
      description='Ache, an asset pipeline automation tool.',
      author='Ben Morris',
      author_email='ben@bendmorris.com',
      url='https://github.com/bendmorris/ache',
      packages=['ache.rules', 'ache'],
      package_dir={
                'ache':'ache'
                },
      entry_points={
        'console_scripts': [
            'ache = ache.__main__:run',
        ],
      },
      requires=[
                'pyparsing',
                ],
      )
