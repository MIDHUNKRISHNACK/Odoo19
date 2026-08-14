from odoo import api, fields, models, tools
from odoo.orm.commands import Command


class ProductTemplate(models.TransientModel):
    _name = "product.template.wizard"

    product_id = fields.Many2one('product.template', string="Product Name", required=True, readonly=True)
    product_ids = fields.One2many('product.product.wizard', inverse_name='product_variant_id')

    @api.model
    def default_get(self, fields):
        values = super().default_get(fields)
        print(values)
        print(values["product_id"])
        product_id = self.env["product.template"].browse(values["product_id"])
        print(product_id)
        variants = self.env["product.product"].search([('product_tmpl_id', '=', product_id.id)])
        print('variants:', variants)
        values["product_ids"] = [
            Command.create({
                "product_id": variant.id
            })
            for variant in variants
        ]

        return values

    def action_update_price(self):
        print("Good Morning")
        print(self.product_id)
        print("kkkkkkkk", self.product_ids)

        for rec in self.product_ids:
            print(rec.product_id)
            print(rec.updated_price)
            print(rec.price)
            if (rec.price != rec.updated_price):
                print(rec.product_id)
                print(rec.updated_price)
                rec.product_id.write({"lst_price": rec.updated_price})
            else:
                continue
