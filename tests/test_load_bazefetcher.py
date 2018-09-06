#!/usr/bin/env python
import os
import camille
import yaml
import datetime

data_dir = os.path.dirname(os.path.abspath(__file__))+"/test_data/bazefetcher/"


def test_all_samples_inside_time_interval_are_loaded():
    tag = '*HS2*'
    start = datetime.datetime(2018, 5, 6)
    end = datetime.datetime(2018, 5, 9)
    result = camille.bazefetcher.load(tag, start, end, base_folder=data_dir)

    assert result.size == 9


def test_time_interval_is_left_closed():
    tag = '*HS2*'
    start = datetime.datetime(2018, 5, 6, 0, 0, 0, 36000)
    end = datetime.datetime(2018, 5, 9)
    result = camille.bazefetcher.load(tag, start, end, base_folder=data_dir)

    assert result.size == 9


def test_time_interval_is_right_open():
    tag = '*HS2*'
    start = datetime.datetime(2018, 5, 6)
    end = datetime.datetime(2018, 5, 7, 0, 0, 0, 439000)
    result = camille.bazefetcher.load(tag, start, end, base_folder=data_dir)

    assert result.size == 8


def test_load_multiple_columns():
    tag = ['*HS2*','*HS*']
    start = datetime.datetime(2018, 5, 6)
    end = datetime.datetime(2018, 5, 9)
    result = camille.bazefetcher.load(tag, start, end, base_folder=data_dir)

    assert result.shape == (9,2)
