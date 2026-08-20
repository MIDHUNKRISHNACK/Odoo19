from odoo import fields,models
class PosConfig(models.Model):
    _inherit = "pos.config"

    is_pos_purchase_limit=fields.Boolean(string="Purchase Limit ", default=False)


