from odoo import api, fields, models, tools
from odoo.orm.commands import Command
class ResPartnerWizard(models.TransientModel):
    _name = "res.partner.wizard"

    sale_order_id= fields.Many2one('sale.order',string="Sale Order")
    partner_id = fields.Many2one('res.partner',readonly=True,string="Customer")
    sale_order_partner_ids= fields.Many2many('sale.order')

    # @api.onchange('partner_id')
    # def _onchange_partner_id(self):
    #     sale_orders= self.env['sale.order'].search([('partner_id','=',self.partner_id),('state','=','draft')])
    #     print(sale_orders)
    #     self.write({'sale_order_partner_ids':sale_orders})
    #     print(self.sale_order_partner_ids)


    def action_merge_sale_order(self):
        print('self.sale_order_partner_ids',self.sale_order_partner_ids)
        print("hello haii")
        print(self.sale_order_id)
        new_sale_order_lines = []

        for record in self.sale_order_partner_ids:
            print(record)
            if record!=self.sale_order_id:
                for rec in record.order_line:
                    new_sale_order_lines.append(Command.create({
                        'product_id':rec.product_id.id,
                        'product_uom_qty':rec.product_uom_qty,
                        'qty_delivered':rec.qty_delivered,
                        'qty_invoiced':rec.qty_invoiced,
                        'product_uom_id':rec.product_uom_id.id,
                        'price_unit':rec.price_unit,
                        'tax_ids':rec.tax_ids,
                        'discount':rec.discount,
                    }))
                    print("new_sale_order_lines = ", new_sale_order_lines)
                record.action_cancel()

            self.sale_order_id.update({
                'order_line': new_sale_order_lines
            })







