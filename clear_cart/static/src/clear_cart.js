import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

console.log('new js triggered');

export class CounterInteraction extends Interaction {
    static selector = '#wrap';
    dynamicContent = {
        "#button_clear": {
            "t-on-click": () => this.newdemo()
        },
    }

    newdemo() {
        console.log("Selector Triggered")
        const result =rpc('/shop/cart/clear')
        const quantity=rpc('/shop/cart/quantity_update').then(window.location.href="/shop/cart")
        console.log (result)
        console.log(quantity)

    }
}
registry.category("public.interactions").add("clear_cart.counterinteraction", CounterInteraction);