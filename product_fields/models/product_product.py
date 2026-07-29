from odoo import api, fields, models
class ProductProduct(models.Model):
    _inherit = "product.product"

    product_brand_id = fields.Many2one('product.product.brand',string="Brand Name")
    product_master_type=fields.Selection([('single','Single Product'),('branded','Branded Product')],string="Master Type",default='single')

