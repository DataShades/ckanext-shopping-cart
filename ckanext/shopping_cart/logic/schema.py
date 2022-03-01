from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.logic.schema import validator_args


@validator_args
def show(not_missing, one_of, unicode_safe):
    return {
        "scope": [not_missing, one_of(["session", "user"])],
        "cart": [not_missing, unicode_safe],
    }


@validator_args
def clear():
    return show()


@validator_args
def pop(not_missing):
    return {
        **show(),
        **{
            "item": [not_missing],
        },
    }


@validator_args
def add(default, convert_to_json_if_string):
    return {**pop(), **{"details": [default("{}"), convert_to_json_if_string]}}
