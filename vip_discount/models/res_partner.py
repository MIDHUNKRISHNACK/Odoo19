from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit='res.partner'


    is_vip=fields.Boolean(string=" VIP ",default=False)
    vip_discount=fields.Integer(string=" VIP Discount ")

