from odoo import fields, models, api
class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_ids=fields.One2many('product.product',inverse_name='product_id')

    def action_open_wizard(self):
        print("hello")

        return {
            'type': 'ir.actions.act_window',
            'name': 'product_template_wizard',
            'res_model': 'product.template.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context':{
                "default_product_id": self.id,

            }
        }
