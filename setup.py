from setuptools import setup, find_packages

from os import path

setup(name='datacroaker',
      version='0.0.1',
      description='Framework for managing data from defined data sources.',
      long_description='Framework for managing data from defined data sources.',
      long_description_content_type='text/markdown',
      url='https://github.com/kaiserpreusse/datacroaker',
      author='Martin Preusse',
      author_email='martin.preusse@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests', 'ftputil', 'graphio', 'dateutil'
      ],
      keywords=['data'],
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License'
      ],
      )
