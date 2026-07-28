from odoo import fields, models
class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_delivery_rating=fields.Boolean(string="Delivery Rating", default=False,config_parameter='purchase_order_delivery_rating.is_delivery_rating')