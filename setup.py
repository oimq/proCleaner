from setuptools import setup, find_packages

setup(name='proCleaner',
      version=2.0,
      author='oimq',
      url='https://github.com/oimq/proCleaner',
      author_email='taep0q@gmail.com',
      description='Data pre-processing module with elasticsearch',
      packages=find_packages(),
      install_requires=['elasticsearch', 'tqdm'],
      zip_safe=False
      )