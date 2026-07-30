from datetime import timedelta
from odoo import api,fields,models
from odoo.orm.commands import Command
class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_prime_partner=fields.Boolean(string="Prime Customer",related="partner_id.is_prime_customer")
    invoice_ids=fields.Many2many('account.move',string="Invoices")

    def brandwise_invoice(self):
        """Function for creating brandwise invoice from sale order on a button click and returning into filtered account.move list view"""
        print(self)
        orderline_records=self.order_line
        print(orderline_records)
        brand_orderline=orderline_records.mapped(lambda brand: brand.product_brand_id)
        print(brand_orderline)
        print(len(brand_orderline))

        for brand in brand_orderline:
                filtered_records=orderline_records.filtered(lambda rec: rec.product_brand_id==brand)
                print(filtered_records)
                product_ids=[]
                for rec in filtered_records:
                    product_ids.append(Command.create({
                        'product_id':rec.product_id.id,
                        'quantity':rec.product_uom_qty,
                        'product_uom_id':rec.product_uom_id.id,
                        'price_unit':rec.price_unit,
                        'product_brand_id':rec.product_brand_id.id,
                    }))
                print('product_ids',product_ids)
                invoices=self.env['account.move'].create({
                    'move_type': 'out_invoice',
                    'partner_id':self.partner_id.id,
                    'invoice_date':self.date_order,
                    'invoice_line_ids':product_ids,
                    'invoice_date_due':(self.date_order+ timedelta(days=10)),

                })
                print(invoices)
                self.update({
                    'invoice_ids': [(fields.Command.link(invoices.id))]
                })

        print(self.invoice_ids)

        return {
            'type': 'ir.actions.act_window',
            'name': 'invoice_list_redirect',
            'res_model': 'account.move',
            'domain': [("id","=",self.invoice_ids.ids)],
            'view_mode': 'list,form',
            'target': 'self',
        }







