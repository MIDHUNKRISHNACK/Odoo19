import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { _t } from "@web/core/l10n/translation";
patch(ProductScreen.prototype, {
   clickCustomAction() {
       this.dialog.add(AlertDialog, {
           title: _t("Custom Action"),
           body: _t("This popup is triggered from a custom Control Button."),
       });
   },
});
