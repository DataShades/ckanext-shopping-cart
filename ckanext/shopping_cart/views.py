from flask import Blueprint


shopping_cart = Blueprint("shopping_cart", __name__)


def page():
    return "Hello, shopping_cart!"


shopping_cart.add_url_rule("/shopping_cart/page", view_func=page)


def get_blueprints():
    return [shopping_cart]
