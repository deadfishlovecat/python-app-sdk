# Copyright © 2017 The Things Network
# Use of this source code is governed by the MIT license that can be found in the LICENSE file.

from setuptools import setup

import io
    # pandoc is not installed, fallback to using raw contents
with io.open('README.rst', encoding="utf-8") as f:
    long_description = f.read()

setup(name='ttnmqtt',
      version='0.9.4',
      description='small package to make mqtt connection to ttn',
      long_description = long_description,
      url = 'https://github.com/TheThingsNetwork/python-app-sdk',
      author='Emmanuelle Lejeail',
      author_email='emmanuelle@thethingsindustries.com',
      license='MIT',
      packages=['ttnmqtt'],
      install_requires=[
          'paho-mqtt',
          'events',
          'pypandoc',
          'grpcio',
          'protobuf',
          'google-api-python-client',
          'google-cloud',
          'os'
      ],
      zip_safe=False)
