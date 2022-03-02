ckan.module("shopping-cart-order", function ($) {
  const { ITEM_ADDED, ITEM_POPPED, CART_REFRESH } = CkanextShoppingCart.events;
  return {
    options: {
      scope: null,
      cart: null,
      item: null,
      details: {},
      inCart: false,
      stateActive: "shopping-cart-order-inside",
      stateInactive: "shopping-cart-order-outside",
      statePending: "shopping-cart-order-pending",
    },
    initialize: function () {
      this.addStateClass();
      this.el.on("click", () => this.processItem());
    },

    processItem: function () {
      const { scope, cart, item, details, inCart } = this.options;
      const payload = { cart, item, scope, details };
      let action, event;
      if (inCart) {
        action = "shopping_cart_pop";
        event = ITEM_ADDED;
      } else {
        action = "shopping_cart_add";
        event = ITEM_POPPED;
      }

      this.pending(true);
      this.sandbox.publish(event, payload);
      this.sandbox.client.call(
        "POST",
        action,
        payload,
        (data) => this._onProcessSucceed(data),
        (resp) => this._onProcessFailed(resp)
      );
    },

    _onProcessSucceed: function (data) {
      const cart = data.result;
      this.pending(false);
      this.options.inCart = cart.some((item) => item.id === this.options.item);
      this.addStateClass();
      this.sandbox.publish(CART_REFRESH, this.options.cart, cart);
    },

    _onProcessFailed: function (resp) {
      this.pending(false);
      console.warn(resp);
    },

    pending: function (enable) {
      this.el.toggleClass(this.options.statePending, enable);
    },
    addStateClass: function () {
      const isActive = this.options.inCart;
      this.el
        .toggleClass(this.options.stateActive, isActive)
        .toggleClass(this.options.stateInactive, !isActive);
    },
  };
});
