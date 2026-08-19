/** @odoo-module */
import { pay } from "@point_of_sale/app/services/pos_store";
import { Dialog } from "@web/core/dialog/dialog";
import { Component } from "@odoo/owl";

export class InfoPopup extends Component {
    static template = "pos_custom_popup.InfoPopup";
    static components = { Dialog };
    // setup() {
    // }
    async confirm() {
       this.props.close()

    }

}

