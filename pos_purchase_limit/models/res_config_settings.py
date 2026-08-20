from odoo import fields, models,api
class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    is_pos_purchase_limit=fields.Boolean(string="Purchase Limit ",related='pos_config_id.is_pos_purchase_limit', readonly=False)



