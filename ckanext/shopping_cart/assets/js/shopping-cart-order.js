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
      this.setState(this.options.inCart);
      this.el.on("click", () => this.processItem());
      this.sandbox.subscribe(CART_REFRESH, (cart, content) =>
        this._onRefresh(cart, content)
      );
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

    _onRefresh: function (cart, content) {
      this.setState(
        cart === this.options.cart &&
          content.some((item) => item.id === this.options.item)
      );
    },
    _onProcessSucceed: function (data) {
      this.pending(false);
      this.sandbox.publish(CART_REFRESH, this.options.cart, data.result);
    },

    _onProcessFailed: function (resp) {
      this.pending(false);
      console.warn(resp);
    },

    pending: function (enable) {
      this.el.toggleClass(this.options.statePending, enable);
    },

    setState: function (isInside) {
      this.options.inCart = isInside;

      this.el
        .toggleClass(this.options.stateActive, isInside)
        .toggleClass(this.options.stateInactive, !isInside);
    },
  };
});
