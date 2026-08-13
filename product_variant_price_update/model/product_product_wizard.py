from odoo import api, fields, models
class ProductProductWizard(models.Model):
    _name = 'product.product.wizard'

    product_variant_id = fields.Many2one('product.template.wizard')
    product_id = fields.Many2one('product.product',string="variants")
    product_name= fields.Char(string="Product Name",related='product_id.display_name')
    price= fields.Float(string="Price",related='product_id.list_price')