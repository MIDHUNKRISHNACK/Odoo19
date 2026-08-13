from odoo import fields, models, api
class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_ids=fields.One2many('product.product',inverse_name='product_id')

    def action_open_wizard(self):
        print("hello")
        product=self.env['product.product'].search([('name','=',self.name)])

        for product in product:
            self.write({'product_ids':[fields.Command.set(product.ids)]})
            self.env['product.template.wizard'].write({'product_ids': [fields.Command.set(product.ids)]})


        print(product)
        print("self.product_ids=",self.product_ids)

        return {
            'type': 'ir.actions.act_window',
            'name': 'product_template_wizard',
            'res_model': 'product.template.wizard',
            'view_mode': 'list',
            'target': 'new',
            'context':{
                "default_product_id": self.id,

            }
        }
