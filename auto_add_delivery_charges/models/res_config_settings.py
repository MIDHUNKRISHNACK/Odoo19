from odoo import fields, models
class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_delivery_charge= fields.Boolean(string="Delivery Charge",default=False,config_parameter='auto_add_delivery_charge.is_delivery_charge')
    delivery_charge=fields.Char(string="Delivery Charge",config_parameter='auto_add_delivery_charge.delivery_charge')

