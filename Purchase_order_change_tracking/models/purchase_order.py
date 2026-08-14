import datetime

from odoo import api, fields, models
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def write(self, vals):
        res = super().write(vals)
        if  self.state=='purchase':
            print(vals)
            print(self)
            note=""
            change=vals.keys()
            for change in change:
                if change!="order_line":
                    note+=str(change+"  has changed to  "+vals[change] +" , ")
                else:
                   for rec in vals[change]:
                       for record in rec:
                           print(record)
                           print(record['product_qty'])



            # self.env['purchase.order.changes.history'].create({
            #         'revision_number': 1,
            #         'modified_user':self.env.user.partner_id.name,
            #         'modified_date':datetime.datetime.now(),
            #         'changes_history':note,
            #     })
        return res



    def action_open_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase_order_history',
            'res_model': 'purchase.order.changes.history',
            'view_mode': 'list',
            }




