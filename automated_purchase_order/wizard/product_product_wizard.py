from odoo import api, fields, models, tools
class product_product_wizard(models.TransientModel):
    _name = "product.product.wizard"

    product_id= fields.Many2one('product.product',string="Product Name",required=True)
    quantity= fields.Float(string="Quantity",required=True)
    price= fields.Float(string="Price",required=True)


    def action_create_po(self):
        print("hello")


