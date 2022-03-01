import ckan.plugins.toolkit as tk


def shopping_cart_required(value):
    if not value or value is tk.missing:
        raise tk.Invalid(tk._("Required"))
    return value


def get_validators():
    return {
        "shopping_cart_required": shopping_cart_required,
    }
