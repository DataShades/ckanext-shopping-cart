import pytest
from ckan.tests.helpers import call_action
from ckanext.shopping_cart import cart


@pytest.mark.usefixtures("clean_cache", "with_plugins", "with_request_context")
@pytest.mark.parametrize("scope", ["user", "session"])
class TestAdd:
    def test_add(self, scope):
        cart = call_action("shopping_cart_add", scope=scope, item="first", cart="test")
        assert cart == {"first": {}}

        cart = call_action("shopping_cart_add", scope=scope, item="second", cart="test", details={1: 2})
        assert cart == {"first": {}, "second": {1: 2}}


@pytest.mark.usefixtures("clean_cache", "with_plugins", "with_request_context")
@pytest.mark.parametrize("scope", ["user", "session"])
class TestPop:
    def test_pop(self, scope):
        call_action("shopping_cart_add", scope=scope, item="first", cart="test")
        cart = call_action("shopping_cart_add", scope=scope, item="second", cart="test", details={1: 2})
        assert cart == {"first": {}, "second": {1: 2}}

        cart = call_action("shopping_cart_pop", scope=scope, item="first", cart="test")
        assert cart == {"second": {1: 2}}

        cart = call_action("shopping_cart_pop", scope=scope, item="second", cart="test")
        assert cart == {}

@pytest.mark.usefixtures("clean_cache", "with_plugins", "with_request_context")
@pytest.mark.parametrize("scope", ["user", "session"])
class TestShow:
    def test_pop(self, scope):
        cart = call_action("shopping_cart_add", scope=scope, item="first", cart="test")
        assert cart == call_action("shopping_cart_show", scope=scope, cart="test")

        cart = call_action("shopping_cart_add", scope=scope, item="second", cart="test", details={1: 2})
        assert cart == call_action("shopping_cart_show", scope=scope, cart="test")

        cart = call_action("shopping_cart_pop", scope=scope, item="first", cart="test")
        assert cart == call_action("shopping_cart_show", scope=scope, cart="test")

        cart = call_action("shopping_cart_pop", scope=scope, item="second", cart="test")
        assert cart == call_action("shopping_cart_show", scope=scope, cart="test")