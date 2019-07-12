from setuptools import setup


setup(name='gcandy',
      version='0.0.1',
      description='Python wrappers for Google REST APIs.',
      url='https://github.com/Marco-Christiani/drive-candy',
      author='Marco Christiani',
      author_email='mchristiani2017@gmail.com',
      license='GPLv3',
      packages=['drivecandy'],
      install_requires=[
          'requests>=2.22.0',
          'PyJWT>=1.7.1',
          'cryptography>=2.7'
      ],
      zip_safe=False)
