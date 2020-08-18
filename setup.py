from setuptools import setup, find_packages

from os import path

setup(name='datacroaker',
      version='0.0.3',
      description='Framework for managing data from defined data sources.',
      url='https://github.com/kaiserpreusse/datacroaker',
      author='Martin Preusse',
      author_email='martin.preusse@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests', 'ftputil', 'graphio', 'python-dateutil'
      ],
      keywords=['data'],
      zip_safe=False,
      classifiers=[
          'Programming Language :: Python',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers'
      ],
      )
