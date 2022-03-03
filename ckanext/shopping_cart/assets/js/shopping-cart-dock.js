ckan.module("shopping-cart-dock", function ($) {
  const { ITEM_ADDED, ITEM_POPPED, CART_REFRESH } = CkanextShoppingCart.events;
  return {
    options: {
      scope: null,
      cart: null,
      counter: ".counter",

      heading: "shopping_cart_dock_heading.html",
      empty: "shopping_cart_dock_empty.html",
      not_empty: "shopping_cart_dock_not_empty.html",
      footer: "shopping_cart_dock_footer.html",
    },

    initialize: async function () {
        this.sandbox.client.endpoint = ckan.LOCALE_ROOT;
      await this.renderBase();
      this.sandbox.subscribe(CART_REFRESH, (cart, content) =>
        this._onRefresh(cart, content)
      );

      this.load();
    },

    _onRefresh: function (cart, content) {
      this.$(this.options.counter).attr("data-count", content.length);
      const payload = this._payload();

      if (content.length) {
        this._render(this.options.not_empty, "body", payload);
      } else {
        this._render(this.options.empty, "body", payload);
      }
    },

    load: function () {
      const payload = this._payload();

      this.sandbox.client.call(
        "POST",
        "shopping_cart_show",
        payload,
        (data) => this._onLoadSucceed(data),
        (resp) => this._onLoadFailed(resp)
      );
    },
    _onLoadSucceed: function (data) {
      this.sandbox.publish(CART_REFRESH, this.options.cart, data.result);
    },

    _onLoadFailed: function (resp) {
      console.warn(resp);
    },

    renderBase: async function () {
      const payload = this._payload();
      return Promise.all([
        this._render(this.options.heading, "heading", payload),
        this._render(this.options.empty, "body", payload),
        this._render(this.options.footer, "footer", payload),
      ]);
    },
    _payload: function () {
      const { scope, cart } = this.options;
      return { scope, cart };
    },
    _render: async function (name, target, payload) {
      return new Promise((s, e) =>

        this.sandbox.client.getTemplate(
          name,
          payload,
          (tpl) => {
            const block = this.$(`.shopping-cart-dock--${target}`).html(tpl);
            $("[data-module]", block).each(function (index, element) {
              ckan.module.initializeElement(this);
            });
            s(block);
          },
          e
        )
      );
    },
  };
});
