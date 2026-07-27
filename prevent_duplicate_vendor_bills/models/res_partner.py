from odoo import api, fields, models
class ResPartner(models.Model):
    _inherit = "res.partner"

    account_ids= fields.One2many("account.move", string="Accounts",inverse_name="partner_id")