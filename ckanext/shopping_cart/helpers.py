from __future__ import annotations

import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector

helper, get_helpers = Collector("shopping_cart").split()


@helper
def show_cart(cart: str, scope: str):
    return tk.get_action("shopping_cart_show")({}, {"cart": cart, "scope": scope})
