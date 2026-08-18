from odoo import fields, models, api
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_wizard_open(self):
        print("hello")
        partner=[]
        for rec in self:
            if rec.state!="draft":
                raise ValidationError("Merging is Only Possible for Draft State Sale Orders")

        if len(self)>1:
            for rec in self:
                if len(partner)==0:
                    partner.append(rec.partner_id)

                elif partner[0]!=rec.partner_id:
                   partner.append(rec.partner_id)

            print(partner)
        else:
            raise ValidationError("Merging is Only Possible for More Than One  Sale Orders")
        if len(partner)>1:
            raise ValidationError("Merging is Only Possible for Same Customer Sale Orders")
        else:

            return {
                'type': 'ir.actions.act_window',
                'name': 'res_partner_wizard',
                'res_model': 'res.partner.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    "default_partner_id": partner[0].id,
                    "default_sale_order_partner_ids": self.ids

                }

            }
