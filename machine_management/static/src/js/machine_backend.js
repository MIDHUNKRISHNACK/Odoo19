import { Interaction } from "@web/public/interaction";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";
import { renderToElement } from "@web/core/utils/render";

console.log('js triggered');

export class CounterInteraction extends Interaction {
    static selector = '.new_user_regisration';
    dynamicContent = {
        "#submit": {
            "t-on-click": () => this.newdemo()
        },
    }
     async newdemo() {
     console.log("Selector Triggered")
     this.name= document.querySelector('#name').value;
     this.type=document.querySelector("#user_type").value;
     this.email=document.querySelector('#email').value
     console.log(this.name)
     console.log(this.type)
         console.log(this.email)
         const result = await rpc('/customer-create', {
             name:this.name,
         type:this.type,
         email:this.email})
         console.log(result)


    }


}
registry.category("public.interactions").add("machine_management.counterinteraction", CounterInteraction);