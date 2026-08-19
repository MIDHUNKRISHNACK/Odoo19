/** @odoo-module */
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/services/pos_store";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";


console.log("this",this);
patch(PosStore.prototype, {
    async pay() {
        console.log("Function Called");
        const current_order = this.getOrder()
        console.log("current_order", current_order)
        console.log("current_order.is_setting_limit", current_order.is_setting_limit)

        if(current_order.is_setting_limit) {
            if (current_order.partner_id) {
                console.log("Continue");
                console.log("partner_id=", current_order.partner_id.id)
                console.log("partner_id=", current_order.partner_id.name)
                if (current_order.partner_id.is_purchase_limit) {
                    console.log("yes")
                    console.log("limit amount=", current_order.partner_id.purchase_limit_amount)
                    console.log("Total Order Amount=", current_order.totalDue)
                    if (current_order.totalDue > current_order.partner_id.purchase_limit_amount) {
                        this.dialog.add(AlertDialog, {
                            title: _t("Sorry.."),
                            body: _t("Exceeded the Customer Limit"),
                        });
                        return false

                    }
                } else {
                    console.log("No")
                }
            } else {
                this.dialog.add(AlertDialog, {
                    title: _t("Sorry.."),
                    body: _t("Choose Any Customer to Move Forward"),
                });
                return false
            }
        }
        else {
            return super.pay()
        }



    },

});
