from setuptools import setup, find_packages


setup(name='pyminicircuits',
      version='0.0.1.dev',
      description='Mini Circuits Device API',
      long_description='',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
      ],
      keywords='minicircuits mini-circuits rf radio',
      url='https://github.com/storborg/pyminicircuits',
      author='Scott Torborg',
      author_email='scott@skysafe.io',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'hidapi',
      ],
      include_package_data=True,
      zip_safe=False,
      entry_points="""\
      [console_scripts]
      minicircuits-attenuator = pyminicircuits.cmd.attenuator:main
      minicircuits-powersensor = pyminicircuits.cmd.powersensor:main
      """)
