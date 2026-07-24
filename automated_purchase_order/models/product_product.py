from odoo import fields, models, api
class ProductProduct(models.Model):
    _inherit = "product.product"


    def button_po_create(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'product_product_wizard',
            'res_model': 'product.product.wizard',
            'view_mode': 'form',
            'target': 'new',
        }


