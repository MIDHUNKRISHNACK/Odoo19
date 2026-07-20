from openpyxl.worksheet import related

from odoo import fields, models


class MachineTransferReportWizard(models.TransientModel):
    _name = "machine.transfer.report.wizard"
    _description = "Machine Transfer Report Wizard"
    machine_transfer_id = fields.Many2one(string="Machine Transfer",comodel_name='machine.machine.transfer')
    from_date = fields.Datetime(string="From Date",required=True)
    to_date = fields.Datetime(string="To Date",required=True)
    # transfer_type=fields.Many2one(string="Transfer Type",related='machine_transfer_id.transfer_type')
    customer_id=fields.Many2one(string="Customer Name",comodel_name="res.partner")
    machine_name_id=fields.Many2one(string="Machine Name",comodel_name="machine.machine")

    def action_print_machine_transfer_report(self):
        domain=[
            ('transfer_date', '>=', self.from_date),
            ('transfer_date', '<=', self.to_date),
        ]
        total_machine_transfers = self.env['machine.machine.transfer'].search(domain)
        print(total_machine_transfers)
        if self.machine_name_id:
            domain.append(('machine_name_id', '=', self.machine_name_id.id))
            domain.append(('customer_name_id','=',self.customer_id.id))

            machine_transfers = self.env['machine.machine.transfer'].search(domain)
            print(machine_transfers)
            data = {
                'from_date': str(self.from_date),
                'to_date': str(self.to_date),
                'customer_id':self.customer_id.name,
                'machine_name_id':self.machine_name_id.machine_name,
                'transfer_ids':machine_transfers.ids,
            }

            print(self.customer_id.name)
            print(self.machine_name_id.machine_name)
            print(machine_transfers.ids)
            return self.env.ref(
                'machine_management.action_machine_transfer_wizard_report'
            ).report_action(None, data=data)
