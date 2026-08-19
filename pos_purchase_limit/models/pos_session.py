from odoo import fields, models,api
class PosSession(models.Model):
    _inherit = "pos.session"

    is_settings_limit = fields.Boolean(string="Purchase Limit Status",compute="_compute_is_settings_limit",default=True)

    def _compute_is_settings_limit(self):
        param = self.env['ir.config_parameter'].sudo()
        print(param)
        settings_rating_status = param.get_param('pos_purchase_limit.is_pos_purchase_limit')
        print(settings_rating_status)
        self.is_settings_limit = settings_rating_status
        print(self.is_settings_limit)

    @api.model
    def _load_pos_data_fields(self, config):
        print('self', self)
        print('config', config)
        result = super()._load_pos_data_fields(config)
        print('result', result)
        print("len of result", len(result))
        result.append('is_settings_limit')
        print("new result", result)
        print("len of result", len(result))
        return result