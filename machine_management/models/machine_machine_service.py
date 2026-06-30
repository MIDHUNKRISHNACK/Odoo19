from odoo import models,fields,api
from odoo.orm.commands import Command

class MachineMachineService(models.Model):
    _name = "machine.machine.service"
    _description="Machine Service"
    _inherit = ['mail.thread', 'mail.activity.mixin']

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
            parts=self.machine_id.product_ids
            self.update({
                'consumed_parts_ids':[(fields.Command.set(parts.ids))]

            })

            print("answer is = ",self.consumed_parts_ids)
            # 'consumed_parts_ids': [(Command.create('id': 'parts.ids',)]



    def  button_case_start(self):
        for rec in self:
            rec.write({"is_case_status":True})
            rec.write({"service_state":"started"})


    def button_case_close(self):
        for rec in self:
            rec.write({"is_case_status":False})
            rec.write({"service_state": "done"})



    def machine_invoice(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'machine_invoice_redirect',
            'res_model': 'account.move',
            'view_mode': 'form',
            'target': 'self',
            'context': {
                '_default_ref':self.customer_id.id
            }

        }


