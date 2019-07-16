from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='gcandy',
      version='0.1.1',
      description='Python wrappers for Google REST APIs.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Marco-Christiani/drive-candy',
      author='Marco Christiani',
      author_email='mchristiani2017@gmail.com',
      license='GPLv3',
      packages=['drivecandy'],
      install_requires=[
          'requests>=2.22.0',
          'PyJWT>=1.7.1',
          'cryptography>=2.7',
          # 'markdown'
      ],
      zip_safe=False)
