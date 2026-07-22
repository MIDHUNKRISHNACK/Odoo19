from odoo import fields, models


class MachineTransferReportWizard(models.TransientModel):
    _name = "machine.transfer.report.wizard"
    _description = "Machine Transfer Report Wizard"
    from_date = fields.Datetime(string="From Date",required=True)
    to_date = fields.Datetime(string="To Date",required=True)
    transfer_type=fields.Selection([('install','Install'),('remove','Remove')],string="Transfer Type")
    customer_ids=fields.Many2many(string="Customer Name",comodel_name="res.partner")
    machine_name_ids=fields.Many2many(string="Machine Name",comodel_name="machine.machine")

    def action_print_machine_transfer_xlsx_report(self):
        print("helloii")

    def action_print_machine_transfer_report(self):
        """ Function for filtering values based on the given fields in wizard and passes to the abstract model """
        print(self.env.cr.dbname)
        customer=tuple(self.customer_ids.ids)
        machine=tuple(self.machine_name_ids.ids)
        print(customer)
        print(machine)
        print(self.transfer_type)
        print(self.to_date.date())


        query="""SELECT DISTINCT machine_machine.machine_name,machine_machine_transfer.transfer_type,res_partner.name,machine_machine_transfer.transfer_date FROM machine_machine_transfer INNER JOIN machine_machine ON machine_machine_transfer.machine_name_id=machine_machine.id INNER JOIN res_partner ON machine_machine_transfer.customer_name_id=res_partner.id
        WHERE machine_machine_transfer.customer_name_id IN %s AND machine_machine_transfer.machine_name_id IN %s AND machine_machine_transfer.transfer_type='%s' AND machine_machine_transfer.transfer_date>='%s' AND machine_machine_transfer.transfer_date<='%s'""" %(customer,machine,self.transfer_type,self.from_date.date(),self.to_date.date())
        self.env.cr.execute(query)
        transfer_ids=self.env.cr.dictfetchall()
        transfer_ids.append({
            "from_date":self.from_date.date(),
            "to_date":self.to_date.date()
        })
        print(transfer_ids)
        print("length of =",len(transfer_ids))



        return self.env.ref(
                'machine_management.action_machine_transfer_wizard_report'
            ).report_action(None, data={'transfer_data':transfer_ids})



        # Method for filtering values using Domain
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
