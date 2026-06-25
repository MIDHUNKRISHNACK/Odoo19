from odoo import fields,models

class machine_machine_parts(models.Model):
    _name = 'machine.machine.products'
    _description = 'Machine Products'

    model_name_id = fields.Many2one('machine.machine', string="Machine Products")
    product_id = fields.Many2one('product.template', string="Machine Parts")
    part_name= fields.Char(string="Machine Parts",related='product_id.display_name')
    part_quantity = fields.Float(string="Quantity")
    part_uom=fields.Selection([('Unit','Unit'),('packages','Packages'),('liter','Liter')],string="Unit of Measure",default='Unit')




