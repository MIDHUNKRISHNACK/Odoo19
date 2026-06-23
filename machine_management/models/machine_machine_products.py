from odoo import fields,models

class machine_machine_products(models.Model):
    _name = 'machine.machine.products'
    _description = 'Machine Products'

    model_name_id = fields.Many2one('machine.machine', string="Machine Products")
    product_id = fields.Many2one('product.template', string="Product Template")
    field_1 = fields.Char()
    field_2 = fields.Char()
    field_3 = fields.Char()
