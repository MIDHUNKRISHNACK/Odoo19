from odoo import fields,models

class machine_machine_tags(models.Model):
    _name = 'machine.machine.tags'
    _description = 'Machine Tags'
    _rec_name = 'machine_tags'


    machine_tags=fields.Char(string="Machine Tags")