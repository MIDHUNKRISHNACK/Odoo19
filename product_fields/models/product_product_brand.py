from odoo import fields, models
class ProductProductBrand(models.Model):
    _name = "product.product.brand"
    _description = "Product Brand"
    _rec_name = "product_brand"

    product_brand=fields.Char(string="Product Brand")