from odoo import api, fields, models, tools
class ProductTemplate(models.TransientModel):
    _name = "product.template.wizard"

    product_id = fields.Many2one('product.product', string="Product Name", required=True, readonly=True)
    product_ids=fields.One2many('product.product.wizard', inverse_name='product_variant_id',compute='_compute_variant_id')

    @api.depends('product_id')
    def _consumed_parts(self):
        parts = self.product_id.product_ids
        self.update({
            'product_ids': [(fields.Command.set(parts.ids))]
        })









