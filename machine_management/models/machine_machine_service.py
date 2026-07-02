from datetime import timedelta

from odoo import models,fields,api,_
from odoo.orm import commands
from odoo.orm.commands import Command
from odoo.orm.fields_temporal import Date


class MachineMachineService(models.Model):
    _name = "machine.machine.service"
    _description="Machine Service"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = "machine_id"


    machine_id=fields.Many2one("machine.machine",string="Machine")
    customer_id=fields.Many2one("res.partner",string="Customer")
    date_of_service=fields.Datetime(string="Date")
    service_description=fields.Char(string="Description")
    internal_note=fields.Html(string="Internal Note")
    service_state=fields.Selection([('open','Open'),('started','Started'),('done','Done'),('cancel','Cancel')])
    company_id=fields.Many2one("res.company",string="Company",store=True,default=lambda self: self.env.user.company_id.id)
    consumed_parts_ids=fields.One2many('machine.machine.products','machine_name_id',string="Parts",compute="_consumed_parts")
    is_case_status=fields.Boolean(string="Is Case Status",default=False)
    tech_person_id=fields.Many2one("res.users",string="Tech Person")

    @api.depends('machine_id')
    def _consumed_parts(self):
        print(self.machine_id.product_ids)
        parts = self.machine_id.product_ids
        self.update({
            'consumed_parts_ids': [(fields.Command.set(parts.ids))]
        })


    def  button_case_start(self):
        for rec in self:
            rec.write({"is_case_status":True})
            rec.write({"service_state":"started"})


    def button_case_close(self):
        for rec in self:
            rec.write({"is_case_status":False})
            rec.write({"service_state": "done"})


    def machine_invoice(self):
       res_id=0
       for rec in self:
            invoice=self.env['account.move'].search([
                    ('partner_id', '=', self.customer_id.id),
                    ('state', '=', 'draft'),], limit=1,)
            print("invoice",invoice.id)
            res_id += invoice.id
            if invoice:
                for record in self.consumed_parts_ids:
                    new_invoice_lines = []
                    new_invoice_lines.append(Command.create({
                           'product_id': record.product_id.id,
                           'quantity': record.part_quantity,
                           'price_unit': record.part_price,
                            }))
                    print("new invoice lines = ",new_invoice_lines)
                    print("result=", record.product_id.id)
                    print("result=", record.product_id)
                    invoice.update({
                        'invoice_line_ids':new_invoice_lines
                    })

                    print("resid=",res_id)
            else:
             print("1",rec.customer_id)
             print("2",rec.customer_id.id)
             print("3",fields.Date.today())
             print("4",rec.consumed_parts_ids.ids)

             invoice_lines = []
             for record in self:
                 for rec in record.consumed_parts_ids:
                   invoice_lines.append(Command.create({
                       'product_id': rec.product_id.id,
                         'quantity': rec.part_quantity,
                         'price_unit': rec.part_price,
                     }))

             invoice=rec.env['account.move'].create({
                  'move_type': 'out_invoice',
                  'partner_id': self.customer_id.id,
                  'invoice_date':self.date_of_service,
                  'invoice_line_ids':invoice_lines,
                  'invoice_date_due': (self.date_of_service + timedelta(days=10)),

             })

             print("invoice",invoice)
             service_product=self.env['product.product'].search([
                 ('name','=','Extra service charge'),
                 ('list_price','=',250)

             ])
             print("service_product",service_product.id)

             service_charge=[]

             service_charge.append(Command.create({
                'product_id':service_product.id,
                'quantity':1,
                'price_unit':service_product.list_price
             }))
             invoice.write({'invoice_line_ids':service_charge})
             res_id+=invoice.id


       return {
            'type': 'ir.actions.act_window',
            'name': 'machine_invoice_redirect',
            'res_model': 'account.move',
            'res_id': res_id,
            'view_mode': 'form',
            'target': 'self',
             }











