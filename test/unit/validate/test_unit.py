"""Tests for the validate methods."""
import pytest

from napalm_base import validate

_compare_getter = [
    (
        {"list": ["\d{2}", 1, 2]},
        [1, 2, 33],
        {u'complies': True, u'extra': [], u'missing': [], u'present': ['\d{2}', 1, 2]}
    ),
    (
        {"list": [1, 2, 3]},
        [1, 2, 3, 4, 5],
        {u'complies': True, u'extra': [], u'missing': [], u'present': [1, 2, 3]}
    ),
    (
        {"list": [2, 1, 3]},
        [3, 2, 1],
        {u'complies': True, u'extra': [], u'missing': [], u'present': [2, 1, 3]}
    ),
    (
        {"list": [1, 2, {"list": [1, 2]}]},
        [1, 2, [1, 2]],
        #  {u'complies': True, u'extra': [], u'missing': [], u'present': [1, 2, [1, 2]]}
        {u'complies': True,
         u'extra': [],
         u'missing': [],
         u'present': [1, 2, {'list': [1, 2]}]}
    ),
    (
        {"list": ['\d{2}', 4, 3]},
        [1, 2, 3],
        {u'complies': False, u'extra': [], u'missing': ['\d{2}', 4], u'present': [3]}
    ),
    (
        {"list": [{"list": [1, 2]}, 3]},
        [1, 2, 3],
        {u'complies': False,
         u'extra': [],
         u'missing': [{'list': [1, 2]}],
         u'present': [3]}
    ),
    (
        {"_mode": "strict", "list": [1, 2, 3]},
        [1, 2, 3],
        {u'complies': True, u'extra': [], u'missing': [], u'present': [1, 2, 3]}
    ),
    (
        {"_mode": "strict", "list": [1, 2, 3]},
        [1, 2, 3, 4, 5],
        {u'complies': False, u'extra': [4, 5], u'missing': [], u'present': [1, 2, 3]}
    ),
    (
        {"_mode": "strict", "list": [2, 1, 3]},
        [3, 2, 1],
        {u'complies': True, u'extra': [], u'missing': [], u'present': [2, 1, 3]}
    ),
    (
        {"_mode": "strict", "list": [1, 2, {"_mode": "strict", "list": [1, 2]}]},
        [1, 2, [1, 2]],
        #  {u'complies': True, u'extra': [], u'missing': [], u'present': [1, 2, [1, 2]]}
        {u'complies': True,
         u'extra': [],
         u'missing': [],
         u'present': [1, 2, {'list': [1, 2]}]}
    ),
    (
        {"_mode": "strict", "list": [4, 3]},
        [1, 2, 3],
        {u'complies': False, u'extra': [1, 2], u'missing': [4], u'present': [3]}
    ),
    (
        {"_mode": "strict", "list": [{"_mode": "strict", "list": [1, 2]}, 3]},
        [1, 2, 3],
        {u'complies': False,
         u'extra': [1, 2],
         u'missing': [{'list': [1, 2]}],
         u'present': [3]}
    ),

    (
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 1, 'b': 2, 'c': 3},
        {u'complies': True,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': True, u'nested': False}}}
    ),
    (
        {'a': 1, 'b': 2, 'c': 3},
        {'a': 2, 'b': 2, 'c': 3},
        {u'complies': False,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'actual_value': 2, u'complies': False, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': True, u'nested': False}}}
    ),
    (
        {'a': 1, 'b': 2, 'c': 3},
        {'b': 1, 'c': 3},
        {u'complies': False,
         u'extra': [],
         u'missing': ['a'],
         u'present': {'b': {u'actual_value': 1, u'complies': False, u'nested': False},
                      'c': {u'complies': True, u'nested': False}}}
    ),
    (
        {'a': 1, 'b': 2, 'c': {"A": 1, "B": 2}},
        {'a': 1, 'b': 2, 'c': {"A": 1, "B": 2}},
        {u'complies': True,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': True, u'nested': True}}}
    ),
    (
        {'a': 1, 'b': 2, 'c': {"A": 1, "B": 2}},
        {'a': 1, 'b': 2, 'd': {"A": 1, "B": 2}},
        {u'complies': False,
         u'extra': [],
         u'missing': ['c'],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False}}}
    ),
    (
        {'a': 1, 'b': 2, 'c': {"A": 3, "B": 2}},
        {'a': 1, 'b': 2, 'c': {"A": 1, "B": 2}},
        {u'complies': False,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': False,
                            u'diff': {u'complies': False,
                                      u'extra': [],
                                      u'missing': [],
                                      u'present': {'A': {u'actual_value': 1,
                                                         u'complies': False,
                                                         u'nested': False},
                                                   'B': {u'complies': True,
                                                         u'nested': False}}},
                            u'nested': True}}}
    ),
    (
        {'a': 1, 'b': 2, 'c': {"A": 3, "B": 2}},
        {'a': 1, 'b': 2, 'c': {"A": 1}},
        {u'complies': False,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': False,
                            u'diff': {u'complies': False,
                                      u'extra': [],
                                      u'missing': ['B'],
                                      u'present': {'A': {u'actual_value': 1,
                                                         u'complies': False,
                                                         u'nested': False}}},
                            u'nested': True}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': 3},
        {'a': 1, 'b': 2, 'c': 3},
        {u'complies': True,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': True, u'nested': False}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': 3},
        {'a': 2, 'b': 2, 'c': 3},
        {u'complies': False,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'actual_value': 2, u'complies': False, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': True, u'nested': False}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': 3},
        {'b': 1, 'c': 3},
        {u'complies': False,
         u'extra': [],
         u'missing': ['a'],
         u'present': {'b': {u'actual_value': 1, u'complies': False, u'nested': False},
                      'c': {u'complies': True, u'nested': False}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': {"_mode": "strict", "A": 1, "B": 2}},
        {'a': 1, 'b': 2, 'c': {"A": 1, "B": 2}},
        {u'complies': True,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': True, u'nested': True}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': {"_mode": "strict", "A": 1, "B": 2}},
        {'a': 1, 'b': 2, 'd': {"A": 1, "B": 2}},
        {u'complies': False,
         u'extra': ['d'],
         u'missing': ['c'],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': {"_mode": "strict", "A": 3, "B": 2}},
        {'a': 1, 'b': 2, 'c': {"A": 1, "B": 2}},
        {u'complies': False,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': False,
                            u'diff': {u'complies': False,
                                      u'extra': [],
                                      u'missing': [],
                                      u'present': {'A': {u'actual_value': 1,
                                                         u'complies': False,
                                                         u'nested': False},
                                                   'B': {u'complies': True,
                                                         u'nested': False}}},
                            u'nested': True}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': {"_mode": "strict", "A": 3, "B": 2}},
        {'a': 1, 'b': 2, 'c': {"A": 1, "C": 4}},
        {u'complies': False,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': False,
                            u'diff': {u'complies': False,
                                      u'extra': ['C'],
                                      u'missing': ['B'],
                                      u'present': {'A': {u'actual_value': 1,
                                                         u'complies': False,
                                                         u'nested': False}}},
                            u'nested': True}}}
    ),
    (
        {"_mode": "strict", 'a': 1, 'b': 2, 'c': {"_mode": "strict", "A": 3, "B": 2}},
        {'a': 1, 'b': 2, 'c': {"A": 1, "C": 4}},
        {u'complies': False,
         u'extra': [],
         u'missing': [],
         u'present': {'a': {u'complies': True, u'nested': False},
                      'b': {u'complies': True, u'nested': False},
                      'c': {u'complies': False,
                            u'diff': {u'complies': False,
                                      u'extra': ['C'],
                                      u'missing': ['B'],
                                      u'present': {'A': {u'actual_value': 1,
                                                         u'complies': False,
                                                         u'nested': False}}},
                            u'nested': True}}}
    ),
]


class TestValidate:
    """Wraps tests."""

    @pytest.mark.parametrize('src, dst, result', _compare_getter)
    def test__compare_getter_list(self, src, dst, result):
        """Test for _compare_getter_list."""
        assert validate._compare_getter(src, dst) == result
