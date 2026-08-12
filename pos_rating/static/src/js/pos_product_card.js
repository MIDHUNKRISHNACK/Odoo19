/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { patch } from "@web/core/utils/patch";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";

console.log("this",this);
patch(ActionpadWidget.prototype, {
       clickNew() {
           const current_order=this.currentOrder.lines
           console.log("current_order",current_order)


       this.dialog.add(AlertDialog, {
           title:_t("Low Rating Products"),
           body: _t("You have Choosed an Low Rating Product in Order "),

       });
   },
});