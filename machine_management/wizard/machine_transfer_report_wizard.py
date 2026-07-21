from odoo import fields, models


class MachineTransferReportWizard(models.TransientModel):
    _name = "machine.transfer.report.wizard"
    _description = "Machine Transfer Report Wizard"
    from_date = fields.Datetime(string="From Date",required=True)
    to_date = fields.Datetime(string="To Date",required=True)
    transfer_type=fields.Selection([('install','Install'),('remove','Remove')],string="Transfer Type")
    customer_ids=fields.Many2many(string="Customer Name",comodel_name="res.partner")
    machine_name_ids=fields.Many2many(string="Machine Name",comodel_name="machine.machine")

    def action_print_machine_transfer_report(self):
        print(self.env.cr.dbname)
        customer=tuple(self.customer_ids.ids)
        machine=tuple(self.machine_name_ids.ids)
        print(customer)
        print(machine)
        print(self.transfer_type)
        print(self.to_date.date())


        query=""" SELECT DISTINCT machine_transfer_report_wizard_res_partner_rel.res_partner_id,machine_machine_machine_transfer_report_wizard_rel.machine_machine_id,machine_machine.machine_name,machine_machine_transfer.transfer_type FROM machine_transfer_report_wizard  INNER JOIN machine_transfer_report_wizard_res_partner_rel ON machine_transfer_report_wizard.id= machine_transfer_report_wizard_res_partner_rel.machine_transfer_report_wizard_id INNER JOIN machine_machine_machine_transfer_report_wizard_rel ON machine_transfer_report_wizard.id=machine_machine_machine_transfer_report_wizard_rel.machine_transfer_report_wizard_id INNER JOIN machine_machine ON machine_machine.id=machine_machine_machine_transfer_report_wizard_rel.machine_machine_id INNER JOIN machine_machine_transfer ON machine_machine.customer_name_id=machine_machine_transfer.customer_name_id
        WHERE machine_transfer_report_wizard_res_partner_rel.res_partner_id IN %s AND machine_machine_machine_transfer_report_wizard_rel.machine_machine_id IN %s AND  machine_machine_transfer.transfer_type='%s' AND machine_machine_transfer.transfer_date>='%s' AND machine_machine_transfer.transfer_date<='%s'""" %(customer,machine,self.transfer_type,self.from_date.date(),self.to_date.date())
        self.env.cr.execute(query)
        transfer_ids=self.env.cr.fetchall()
        print(transfer_ids)
        print("length of =",len(transfer_ids))


        return self.env.ref(
                'machine_management.action_machine_transfer_wizard_report'
            ).report_action(None, data=transfer_ids)


        # domain=[
        #     ('transfer_date', '>=', self.from_date),
        #     ('transfer_date', '<=', self.to_date),
        # ]
        # total_machine_transfers = self.env['machine.machine.transfer'].search(domain)
        # print(total_machine_transfers)
        # if self.machine_name_id:
        #     domain.append(('machine_name_id', '=', self.machine_name_id.id))
        #     domain.append(('customer_name_id','=',self.customer_id.id))
        #
        #     machine_transfers = self.env['machine.machine.transfer'].search(domain)
        #     print(machine_transfers)
        #     data = {
        #         'from_date': str(self.from_date),
        #         'to_date': str(self.to_date),
        #         'customer_id':self.customer_id.name,
        #         'machine_name_id':self.machine_name_id.machine_name,
        #         'transfer_ids':machine_transfers.ids,
        #     }
        #
        #     print(self.customer_id.name)
        #     print(self.machine_name_id.machine_name)
        #     print(machine_transfers.ids)
        #     return self.env.ref(
        #         'machine_management.action_machine_transfer_wizard_report'
        #     ).report_action(None, data=data)
