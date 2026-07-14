from openpyxl.worksheet import related

from odoo import fields, api, models


class Saleorder(models.Model):
    _inherit ='sale.order'

    is_vip_discount_apply=fields.Boolean(string=" Apply Discount",default=False)
    vip_discount=fields.Integer(string=" VIP Discount",related="partner_id.vip_discount",store=True)

    # @api.onchange('partner_id')
    # def onchange_partner_id(self):
    #     """Function For Setting discount value from related partner """
    #     self.write({'vip_discount':self.partner_id.vip_discount})

    @api.onchange('is_vip_discount_apply','order_line')
    def onchange_is_vip_discount_apply(self):
        """Function For Applying Discount for every products in orderline"""
        if self.is_vip_discount_apply:
          for rec in self.order_line:
             rec.discount = self.vip_discount

        else:
            for rec in self.order_line:
                rec.discount = 0


    # code for calculating percentage of discount in order to float value

    # @api.onchange('is_vip_discount_apply')
    # def onchange_is_vip_discount_apply(self):
    #     for rec in self.order_line:
    #         rec.discount =100-(((rec.price_unit-self.vip_discount)/rec.price_unit)*100)
    #         self.write({'is_vip_status':True})

