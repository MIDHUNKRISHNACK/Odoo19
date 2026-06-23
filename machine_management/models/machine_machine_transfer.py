from odoo import fields, models

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


    def button_transfer(self):
        """Function For Actions that performing while clicking the transfer button"""

        for rec in self:
          if rec.machine_name_id:
                rec.transfer_ribbon_id=True
                rec.machine_name_id.status='inservice'
                rec.machine_name_id.customer_name_id=rec.customer_name_id



