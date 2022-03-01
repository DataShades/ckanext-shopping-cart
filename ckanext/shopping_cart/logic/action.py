from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckan.logic import validate
from ckanext.toolbelt.decorators import Collector
from . import schema
from .. import cart

action, get_actions = Collector("shopping_cart").split()


@action
@validate(schema.add)
def add(context, data_dict):
    tk.check_access("shopping_cart_add", context, data_dict)

    c = cart.get_cart(data_dict["scope"], context)
    c.restore(data_dict["cart"])

    c.add(data_dict["item"], data_dict["details"])
    c.save(data_dict["cart"])
    return c.show()


@action
@validate(schema.add)
def pop(context, data_dict):
    tk.check_access("shopping_cart_pop", context, data_dict)

    c = cart.get_cart(data_dict["scope"], context)
    c.restore(data_dict["cart"])

    c.pop(data_dict["item"])
    c.save(data_dict["cart"])
    return c.show()


@action
@tk.side_effect_free
@validate(schema.show)
def show(context, data_dict):
    tk.check_access("shopping_cart_show", context, data_dict)

    c = cart.get_cart(data_dict["scope"], context)
    c.restore(data_dict["cart"])

    return c.show()


@action
@tk.side_effect_free
@validate(schema.clear)
def clear(context, data_dict):
    tk.check_access("shopping_cart_clear", context, data_dict)

    c = cart.get_cart(data_dict["scope"], context)
    c.clear()
    c.save(data_dict["cart"])

    return c.show()
