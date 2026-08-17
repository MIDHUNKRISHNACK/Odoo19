from odoo import fields, models, api
class ResPartner(models.Model):
    _inherit = "res.partner"


    def action_open_wizard(self):
        print("hello")
        return {
            'type': 'ir.actions.act_window',
            'name': 'res_partner_wizard',
            'res_model': 'res.partner.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                "default_partner_id": self.id,

            }
        }

