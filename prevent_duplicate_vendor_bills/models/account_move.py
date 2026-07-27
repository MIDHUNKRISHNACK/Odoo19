from odoo import api, fields, models, tools,_
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def create(self, vals_list):
        res = super(AccountMove, self).create(vals_list)

        print(res)
        vendor_bills = res.partner_id.account_ids
        print(vendor_bills)
        total_amt = res.amount_total
        print(total_amt)
        filtered = vendor_bills.filtered(
            lambda bill: bill.amount_total == res.amount_total or bill.ref==res.ref)
        print(filtered)

        error="Duplicate bill orders found in record"
        if len(filtered) > 0:
            for bill in filtered:
                if bill.state == "draft":
                    error+=""
                else:
                    error=error + " " +str(bill.name)

            raise UserError(_(error))

        return res





    # def action_post(self):
    #     res=super().action_post()
    #     vendor_bills=self.partner_id.account_ids
    #     print(vendor_bills)
    #
    #     filtered=vendor_bills.filtered(lambda bill:bill.ref==self.ref)
    #     print(filtered)
    #     raise UserError(_("Duplicate purchase orders found!"))

