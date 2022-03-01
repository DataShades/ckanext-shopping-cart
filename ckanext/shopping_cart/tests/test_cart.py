import pytest
from ckanext.shopping_cart import cart


class TestCart:
    def test_restore(self, cart):
        cart.restore("restore")
        assert not cart

        cart.add("hello", {})
        cart.restore("restore")
        assert not cart

        cart.add("hello", {})
        cart.save("restore")

        cart.restore("fake")
        assert not cart

        cart.restore("restore")
        assert cart
