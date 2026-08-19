/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import {InfoPopup} from "./new_alert_dialog";
import { makeAwaitable } from "@point_of_sale/app/utils/make_awaitable_dialog";
import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

console.log("this",this);
patch(PosStore.prototype, {
    async pay() {
        console.log("Function Called");
        const current_order = this.getOrder()
        console.log("current_order", current_order)
        for (const line of current_order.lines) {
            console.log("product_id", line.product_id)
            console.log("product_rating", line.product_id.product_rating)
               if (line.product_id.product_rating == 'two' || line.product_id.product_rating == 'three') {
                await makeAwaitable(this.dialog, InfoPopup, {
                       title: _t("Custom Popup!"),
                   });
                   console.log("hello")
                   return false
               }
           }

          return super.pay()



    },

});

patch(PaymentScreen.prototype, {
    async validateOrder() {
        console.log("Validate worked");
        console.log("this in product screen",this);
        console.log("this.current_order.lines",this.currentOrder.lines);
        const rating=[];
        for (const line of this.currentOrder.lines) {
            console.log("product_id", line.product_id)
            console.log("product_rating", line.product_id.product_rating)
            if(line.product_id.product_rating == 'six'){
                rating[0]=line.product_id;

            }
            else{
                rating.push(line.product_id);
            }
        }
        console.log("rating",rating)
        if (rating.length == 1){
            for (const id of this.paymentLines) {
               console.log("this.paymentid",id.payment_method_id.id );
               if (id.payment_method_id.id==6){
                   this.dialog.add(AlertDialog,{
                        title: _t("Sorry.."),
                        body:_t("For Every Product with Five Star Rating Only Card Payment is Available"),
                   });
                   return false
               }
        }

        }

        return super.validateOrder()
    }
});