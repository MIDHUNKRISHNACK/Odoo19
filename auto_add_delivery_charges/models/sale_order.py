from odoo import fields, models, api
from odoo.orm.commands import Command


class SaleOrder(models.Model):
    _inherit = "sale.order"


    def action_confirm(self):
        """ Adding condition to current button confirm action """
        print(self)
        delivery_product = self.env.ref('auto_add_delivery_charges.delivery_product')
        print(delivery_product)
        print(delivery_product.name)
        print(self.order_line)

        if self.amount_untaxed < 1500:
            self.order_line.create({
                    'order_id':self.id,
                    'product_id': delivery_product.id,
                    'name': delivery_product.name,
                    'product_uom_qty': 1,
                    'price_unit': delivery_product.list_price,

            })
        res=super().action_confirm()
        return res
