from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='my315ok.socialorgnization',
      version=version,
      description="a social orgnization management content type based dexterity",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='python plone',
      author='Adam tang',
      author_email='yuejun.tang@gmail.com',
      url='https://github.com/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['my315ok'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.directives.dexterity',
          'plone.app.dexterity',
          'collective.autopermission',
          # -*- Extra requirements: -*-
          'collective.dexteritytextindexer',
          'z3c.caching',          
      ],
      extras_require={
          'test': ['plone.app.testing',]
          },            
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
#      setup_requires=["PasteScript"],
#      paster_plugins = ["ZopeSkel"],

      )
