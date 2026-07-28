from odoo import api, fields, models
class ResPartner(models.Model):
    _inherit= "res.partner"

    purchase_order_ids=fields.One2many("purchase.order",inverse_name="partner_id")
    vendor_rating=fields.Char("Vendor Rating",readonly=True)


    def action_open_purchase_order_list_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase_order_list_view',
            'res_model': 'purchase.order',
            'domain': [('partner_id', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'self',
        }



