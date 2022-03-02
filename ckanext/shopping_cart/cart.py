from __future__ import annotations

import abc
import pickle
import dataclasses
from typing import Any, Iterable, Optional, OrderedDict

import ckan.lib.redis as redis
import ckan.plugins.toolkit as tk
from ckan.common import session

CONFIG_CART_FACTORY = "ckanext.shopping_cart.factory.default"
DEFAULT_CART_FACTORY = "redis"


def get_cart(scope: str, context: dict[str, Any]):
    factory = factories[
        tk.config.get(CONFIG_CART_FACTORY, DEFAULT_CART_FACTORY)
    ]
    cart = factory()

    cart.identify(scope, context)
    return cart

@dataclasses.dataclass
class Item:
    id: str
    details: dict[str, Any] = dataclasses.field(default_factory=dict)


class Cart(abc.ABC):
    id: Optional[str] = None
    content: Any

    def __init__(self):
        self.clear()

    def clear(self):
        self.content = {}

    def identify(self, scope: str, context: dict[str, Any]):
        id_: str = context["user"]
        if scope == "session":
            id_ = getattr(session, "id", "")

        self.id = id_

    def add(self, item: Any, details: dict[str, Any]):
        self.content[item] = details

    def pop(self, item: Any):
        return self.content.pop(item, None)

    def show(self):
        return [{"id": id, "details": details} for id, details in self.content.items()]

    def __bool__(self):
        return bool(self.content)

    @abc.abstractmethod
    def restore(self, key: str):
        pass

    @abc.abstractmethod
    def save(self, key: str):
        pass

    @abc.abstractmethod
    def drop(self, key: str):
        pass


class RedisCart(Cart):
    def __init__(self):
        super().__init__()
        self.conn = redis.connect_to_redis()
        site_id = tk.config["ckan.site_id"]
        self.prefix = f"ckan:{site_id}:ckanext:shopping_cart:{self.id}"

    def restore(self, key: str):
        data = self.conn.get(self.prefix + key)
        if not data:
            self.clear()
            return
        self.content = pickle.loads(data)

    def save(self, key: str):
        self.conn.set(self.prefix + key, pickle.dumps(self.content))

    def drop(self, key: str):
        self.conn.delete(self.prefix + key)


class SessionCart(Cart):
    def __init__(self):
        super().__init__()
        self.session = session

    def restore(self, key: str):
        data = self.session.get(f"shopping_cart:{key}")
        if not data:
            self.clear()
            return
        self.content = data

    def save(self, key: str):
        self.session[f"shopping_cart:{key}"] = self.content

    def drop(self, key: str):
        self.session.pop(f"shopping_cart:{key}", None)


class FakeSessionCart(SessionCart):
    def __init__(self):
        super().__init__()

        if "shopping_cart_session" not in tk.g:
            tk.g.shopping_cart_session = {}
        self.session = tk.g.shopping_cart_session


factories = {
    "redis": RedisCart,
    "session": SessionCart,
}
