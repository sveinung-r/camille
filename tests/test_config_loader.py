#!/usr/bin/env python
import pytest
import os
import camille
import yaml

data_dir = os.path.dirname(os.path.abspath(__file__))+"/test_data/bazefetcher/"

def test_load_config():
    conf = """
           tag: [.*HS2.*]
           start: 2018-05-06T00:00:00+00:00
           end: 2018-05-08
           processor:
             fft:
               inverse: False
           input:
             bazefetcher:
               base_folder: {}
           join: outer
           interpolation: nearest
           """.format( data_dir )
    conf = yaml.load(conf)

    c = camille.load_config(conf)
    result = camille.run(c)
    print(result.size)
    assert False
