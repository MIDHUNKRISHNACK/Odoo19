from odoo import fields, models
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_brand_id = fields.Many2one('product.product.brand', string="Product Brand")

