
from odoo import fields, models, api,_
from odoo.orm import commands
from odoo.orm.commands import Command


class AccountMove(models.Model):
    _inherit = "account.move"

    purchase_order_id=fields.Integer("Purchase Bill")


    def button_po_create(self):
        order_lines = []
        for record in self:
            for rec in record.invoice_line_ids:
                order_lines.append(Command.create({
                    'product_id': rec.product_id.id,
                    'product_qty': rec.quantity,
                    'qty_received': rec.quantity,
                    'qty_invoiced': rec.quantity,
                    'price_unit': rec.price_unit,
                    'price_subtotal': rec.price_subtotal,
                }))
        purchase_order=self.env['purchase.order'].create({
            'partner_id':self.partner_id.id,
            'date_approve':self.date,
            'date_planned':self.invoice_date,
            'order_line':order_lines,
        })

        self.purchase_order_id=purchase_order.id
        purchase_order.button_confirm()
        # match_lines = self.env['purchase.bill.line.match'].search([('partner_id', '=', self.partner_id)])
        # match_lines.action_match_lines()


