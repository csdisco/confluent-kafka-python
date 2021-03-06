#!/usr/bin/env python

import os
from setuptools import setup, find_packages
from distutils.core import Extension
import sys

INSTALL_REQUIRES = list()

if sys.version_info[0] < 3:
    avro = 'avro'
    INSTALL_REQUIRES.extend(['futures', 'enum34'])
else:
    avro = 'avro-python3'

module = Extension('confluent_kafka.cimpl',
                   libraries=['rdkafka'],
                   sources=['confluent_kafka/src/confluent_kafka.c',
                            'confluent_kafka/src/Producer.c',
                            'confluent_kafka/src/Consumer.c',
                            'confluent_kafka/src/Metadata.c',
                            'confluent_kafka/src/AdminTypes.c',
                            'confluent_kafka/src/Admin.c'])


install_requirements_path = os.environ.get('INSTALL_REQUIREMENTS_PATH_OVERRIDE',
                                           os.path.dirname(__file__))


def get_install_requirements(path):
    content = open(os.path.join(install_requirements_path, path)).read()
    return [
        req
        for req in content.split("\n")
        if req != '' and not req.startswith('#')
    ]


version = os.getenv('TRAVIS_TAG') or os.getenv('BUILD_VERSION')
if not version:
    build_number = os.getenv('TRAVIS_BUILD_NUMBER')
    if build_number:
        version = '0.0.' + str(build_number)
    else:
        version = '0.0.1'

print("environment is" + str(os.environ))
print("version is " + str(version))


setup(name='disco.confluent-kafka',
      version=version,
      description='Confluent\'s Apache Kafka client for Python',
      author='Confluent Inc',
      author_email='support@confluent.io',
      url='https://github.com/confluentinc/confluent-kafka-python',
      ext_modules=[module],
      packages=find_packages(exclude=("tests", "tests.*")),
      data_files=[('', ['LICENSE.txt'])],
      install_requires=INSTALL_REQUIRES,
      extras_require={
          'avro': ['fastavro', 'requests', avro],
          'dev': get_install_requirements("test-requirements.txt")
      })
