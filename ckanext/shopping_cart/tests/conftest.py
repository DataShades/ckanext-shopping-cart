import pytest

import ckan.lib.redis as redis
from ..cart import RedisCart, FakeSessionCart


@pytest.fixture(
    params=[
        RedisCart,
        FakeSessionCart,
    ]
)
def cart(clean_cache, with_request_context, request):
    cart = request.param()
    return cart


@pytest.fixture(scope="session")
def reset_cache():
    def reset():
        conn = redis.connect_to_redis()
        keys = conn.keys("*")
        if keys:
            conn.delete(*keys)

    return reset


@pytest.fixture
def clean_cache(reset_cache):
    reset_cache()
