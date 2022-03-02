ckan.module("shopping-cart-dock", function ($) {
  const { ITEM_ADDED, ITEM_POPPED, CART_REFRESH } = CkanextShoppingCart.events;

  return {
    options: {},
    cart: {},

    initialize: function () {},
  };
});
