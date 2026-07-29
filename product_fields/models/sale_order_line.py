from odoo import api, fields, models
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    product_brand_id = fields.Many2one('product.product.brand',string="Product Brand",related='product_id.product_brand_id')
