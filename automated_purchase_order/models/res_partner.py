from odoo import api,fields,models,exceptions
class ResPartner(models.Model):
    _inherit = 'res.partner'

    purchase_order_ids = fields.One2many(inverse_name='partner_id',comodel_name='purchase.order')

