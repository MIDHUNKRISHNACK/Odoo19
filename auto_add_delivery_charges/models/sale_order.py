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
        param = self.env['ir.config_parameter'].sudo()
        print(param)
        delivery_adding_status=param.get_param('auto_add_delivery_charge.is_delivery_charge')
        untaxed_amount=param.get_param('auto_add_delivery_charge.delivery_charge')
        print("status = ",delivery_adding_status)
        print("untaxed_amount = ",untaxed_amount)

        if delivery_adding_status and self.amount_untaxed < float(untaxed_amount):
               self.order_line.create({
                'order_id':self.id,
                'product_id': delivery_product.id,
                'name': delivery_product.name,
                'product_uom_qty': 1,
                'price_unit': delivery_product.list_price,

        })

        res=super().action_confirm()
        return res







