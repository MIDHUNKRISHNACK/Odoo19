from odoo import fields, models,api
from odoo.fields import Command
from odoo.orm.commands import Command


class machine_machine_transfer(models.Model):
    _name = 'machine.machine.transfer'
    _description = 'Machine Transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'machine_name_id'

    machine_name_id=fields.Many2one('machine.machine',string="Machine Name")
    serial_number_id=fields.Char(string='SerialNumber',related="machine_name_id.serial_number")
    transfer_date=fields.Datetime(string="Transfer Date")
    transfer_type=fields.Selection([('install','Install'),('remove','Remove')],string="Transfer Type",default='install')
    customer_name_id=fields.Many2one('res.partner',string="Customer Name")
    transfer_id=fields.Char(string="Transfer")
    company_id=fields.Many2one('res.company',string="Company", default=lambda self: self.env.user.company_id.id)
    instructions=fields.Html(string="Instruction")
    transfer_ribbon_id=fields.Boolean(default=False)
    domain=fields.Char(string="Domain",compute="_compute_domain")
    machine_name_test=fields.Many2one('machine.machine',string="Machine Name")
    transfer_type_test=fields.Selection([('install','Install'),('remove','Remove')],string="Transfer Type",default='install')
    alternate_machine_ids=fields.Many2many('machine.machine','machine_alt_rel',compute='_compute_alternate_machine_ids')



    @api.depends('transfer_type_test')
    def _compute_alternate_machine_ids(self):
        # self.alternate_machine_ids=False
        if self.transfer_type_test == 'install' and [('status','==','active')]:
            self.write({
                'alternate_machine_ids': [Command.link(self.machine_name_test.id)]
            })




    def button_transfer(self):
        """Function For Actions that performing while clicking the transfer button"""
        for rec in self:
          if rec.machine_name_id:
                print("rec", rec)
                print("new", rec.machine_name_id)

                rec.machine_name_id.write({'customer_name_id': rec.customer_name_id.id, })
                rec.write({"transfer_ribbon_id":True})

                rec.machine_name_id.write({'status':'inservice'})





    @api.depends("transfer_type")

    def _compute_domain(self):
        """Function For Dynamic domain """
        if self.transfer_type == 'install':
            self.domain=[('status','=','active')]
        elif self.transfer_type == 'remove':
            self.domain=[('status','=','inservice')]
        else:
            self.domain=[]












