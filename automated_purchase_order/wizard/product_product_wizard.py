from odoo import api, fields, models, tools
class product_product_wizard(models.TransientModel):
    _name = "product.product.wizard"

    product_id= fields.Many2one('product.product',string="Product Name",required=True,readonly=True)
    quantity= fields.Float(string="Quantity",required=True)
    price= fields.Float(string="Price",required=True)

    def action_create_po(self):
        """Function to checking whether there is any open rfq if it is then add a new orderline with given product otherwise create a new purchase order"""
        print("product_id", self.product_id)
        vendor_ids=self.product_id.seller_ids.partner_id
        print("vendor_id", vendor_ids)
        top_vendor_id=vendor_ids[0]
        purchase_order_ids=top_vendor_id.purchase_order_ids
        print(purchase_order_ids)

        purchase_order=purchase_order_ids.filtered(lambda po:po.state=='draft')
        print("purchase_order",purchase_order)

        if purchase_order:

            purchase_order[0].write({
                'order_line':[fields.Command.create({
                    "product_id":self.product_id.id,
                    "product_qty":self.quantity,
                    "price_unit":self.price,
                })]
            })
            purchase_order[0].button_confirm()
            return {
                'type': 'ir.actions.act_window',
                'name': 'purchase_order',
                'res_model': 'purchase.order',
                'view_mode': 'form',
                'res_id': purchase_order[0].id,

            }
        else:
            new_po=self.env['purchase.order'].create({
                'partner_id':top_vendor_id.id,
                'order_line': [fields.Command.create({
                    "product_id": self.product_id.id,
                    "product_qty": self.quantity,
                    "price_unit": self.price,
                })]
            })
            new_po.button_confirm()
            return{
            'type': 'ir.actions.act_window',
            'name': 'purchase_order',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'res_id': new_po.id,

        }



