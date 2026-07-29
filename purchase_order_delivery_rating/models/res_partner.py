from odoo import api, fields, models
class ResPartner(models.Model):
    _inherit= "res.partner"

    purchase_order_ids=fields.One2many("purchase.order",inverse_name="partner_id")
    vendor_rating=fields.Selection([('star0',' '),('star1',' * '),('star2',' * * '),('star3',' * * * '),('star4',' * * * * '),('star5',' * * * * * ')],readonly=True)
    status_rating=fields.Boolean(string="Rating Status",default=lambda self: self.env['ir.config_parameter'].get_param('purchase_order_delivery_rating.is_delivery_rating'))

    def action_open_purchase_order_list_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase_order_list_view',
            'res_model': 'purchase.order',
            'domain': [('partner_id', '=', self.id)],
            'view_mode': 'list,form',
            'target': 'self',
        }



