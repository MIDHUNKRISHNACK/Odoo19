from odoo import fields,models,api

class Saleorderlines(models.Model):
    _inherit ='sale.order.line'

    milestone=fields.Integer(string="Milestone")


