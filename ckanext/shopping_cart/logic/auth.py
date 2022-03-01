from __future__ import annotations

from ckan import authz
import ckan.plugins.toolkit as tk
from ckanext.toolbelt.decorators import Collector

auth, get_auth_functions = Collector("shopping_cart").split()


@auth
@tk.auth_allow_anonymous_access
def show(context, data_dict):
    if data_dict["scope"] == "user" and not context["user"]:
        return {"success": False}
    return {"success": True}


@auth
@tk.auth_allow_anonymous_access
def pop(context, data_dict):
    return authz.is_authorized("shopping_cart_show", context, data_dict)


@auth
@tk.auth_allow_anonymous_access
def add(context, data_dict):
    return authz.is_authorized("shopping_cart_show", context, data_dict)


@auth
@tk.auth_allow_anonymous_access
def clear(context, data_dict):
    return authz.is_authorized("shopping_cart_show", context, data_dict)
