from setuptools import setup, find_packages

setup(name='mos-interface',
      zip_safe=False,
      version='0.1.1',
      author='Fuinn',
      url='https://github.com/Fuinn/mos-interface-py',
      description='Python interface of MOS',
      license='BSD 3-Clause License',
      packages=find_packages(),
      include_package_data=True,
      classifiers=['Development Status :: 4 - Beta',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: Microsoft :: Windows',
                   'Operating System :: MacOS',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3.6'],
      install_requires=["numpy>=1.14.3",
                        "scipy>=1.1.0",
                        "requests>=2.22.0"])