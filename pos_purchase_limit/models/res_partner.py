from odoo import fields, models,api
class ResPartner(models.Model):
    _inherit = "res.partner"

    is_purchase_limit=fields.Boolean(string="Purchase Limit",default=False)
    purchase_limit_amount=fields.Float(string="Purchase Limit Amount")

    @api.model
    def _load_pos_data_fields(self, config):
        """ Load data fields to POS """
        print('self', self)
        print('config', config)
        result = super()._load_pos_data_fields(config)
        print('result', result)
        print("len of result", len(result))
        result.append('is_purchase_limit')
        result.append('purchase_limit_amount')
        print("new result", result)
        print("len of result", len(result))
        return result


