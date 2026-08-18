/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import {InfoPopup} from "./new_alert_dialog";

console.log("this",this);
patch(PosStore.prototype, {
    async pay() {
        console.log("Function Called");
        const current_order = this.getOrder()
        var count = 0
        console.log("current_order", current_order)
        for (const line of current_order.lines) {
            console.log("product_id", line.product_id)
            console.log("product_rating", line.product_id.product_rating)
               if (line.product_id.product_rating == 'two' || line.product_id.product_rating == 'three') {
                   count += 1
                   this.dialog.add(InfoPopup, {
                       title: _t("Custom Popup!"),
                   });

               }
           }
           console.log("count",count)
           if (count==0){
               return super.pay()
           }


    },

});


// console.log("this",this);
// patch(ControlButtons.prototype, {
//       onClickMessage(){
//            const current_order=this.currentOrder
//            console.log("current_order.lines",current_order.lines)
//            for(const line of current_order.lines){
//                console.log("product_id",line.product_id)
//                console.log("product_rating",line.product_id.product_rating)
//                if(line.product_id.product_rating=='one' || line.product_id.product_rating=='two'){
//                    this.dialog.add(AlertDialog, {
//                    title:_t("Low Rating Products"),
//                    body: _t("You have Choosed an Low Rating Product in Order "),
//
//                 });
//
//                }
//            }

//
//
//    },
// });
