from odoo import models,fields

class machine_machine_types(models.Model):
    _name = 'machine.machine.types'
    _description = 'Machine Types'
    _rec_name = 'machine_type'

    machine_type=fields.Char(string="Machine Type")