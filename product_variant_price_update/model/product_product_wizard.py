from odoo import api, fields, models
class ProductProductWizard(models.TransientModel):
    _name = 'product.product.wizard'

    product_variant_id = fields.Many2one('product.template.wizard')
    product_id = fields.Many2one('product.product',string="variants")
    product_name= fields.Char(string="Product Name",related='product_id.display_name')
    price= fields.Float(string="Price",related='product_id.lst_price')
    updated_price= fields.Float(string="Updated Price",compute="_compute_updated_price",readonly=False,store=True)

    @api.depends('price')
    def _compute_updated_price(self):
        for record in self:
            record.updated_price=record.product_id.lst_price





