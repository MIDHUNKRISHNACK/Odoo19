from odoo import fields, models,api
class ResPartner(models.Model):
    _inherit = "res.partner"

    is_purchase_limit=fields.Boolean(string="Purchase Limit",default=False)
    purchase_limit_amount=fields.Float(string="Purchase Limit Amount")
    is_setting_limit=fields.Boolean(string="Setting Limit",compute="_compute_is_setting_limit",invisible=True)


    def _compute_is_setting_limit(self):
        param = self.env['ir.config_parameter'].sudo()
        print(param)
        settings_rating_status = param.get_param('pos_purchase_limit.is_pos_purchase_limit')
        print(settings_rating_status)
        self.is_setting_limit = settings_rating_status
        print(self.is_setting_limit)

    @api.model
    def _load_pos_data_fields(self, config):
        print('self', self)
        print('config', config)
        result = super()._load_pos_data_fields(config)
        print('result', result)
        print("len of result", len(result))
        result.append('is_purchase_limit')
        result.append('purchase_limit_amount')
        result.append('is_setting_limit')
        print("new result", result)
        print("len of result", len(result))
        return result


