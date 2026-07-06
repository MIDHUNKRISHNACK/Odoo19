from odoo import models,fields

class machine_machine_service_freequency(models.Model):
    _name = 'machine.machine.service.frequency'
    _description = 'Machine Service Frequency'
    _rec_name = 'machine_service_frequency'

    machine_service_frequency=fields.Char(string="Machine Service Frequency Type")