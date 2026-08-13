from odoo import fields, models
class ProductProduct(models.Model):
    _inherit = 'product.product'

    product_id = fields.Many2one('product.template', string="Product Template")
