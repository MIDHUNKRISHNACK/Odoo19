from odoo import fields, models, api
class ProductProduct(models.Model):
    _inherit = "product.template"

    product_rating=fields.Selection([('one','1'),('two','2'),('three','3'),('four','4'),('five','5'),('six','6')])

    @api.model
    def _load_pos_data_fields(self, config):
        print('self', self)
        print('config', config)
        result = super()._load_pos_data_fields(config)
        print('result', result)
        print("len of result", len(result))
        result.append('product_rating')
        print("new result", result)
        print("len of result", len(result))
        return result

