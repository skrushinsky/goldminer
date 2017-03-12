
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

version = '0.1'

setup(name='goldminer',
      version=version,
      description="Quotes scrapper",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Sergey Krushinsky',
      author_email='krushinsky@gmail.com',
      url='',
      license='Commercial',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
            'lxml',
            'requests',
            'beautifulsoup4',
      ],
      test_requires=['nose'],
      scripts = ['scripts/main.py'],      
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
