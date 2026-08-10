import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

console.log('new js triggered');

export class CounterInteraction extends Interaction {
    static selector = '#wrap';
    dynamicContent = {
        "#button_clear": {
            "t-on-click": () => this.newdemo()
        },
    }

    async newdemo() {
        console.log("Selector Triggered")
        const result = await rpc('/shop/cart/clear')
        console.log(result)
    }
}
registry.category("public.interactions").add("clear_cart.counterinteraction", CounterInteraction);