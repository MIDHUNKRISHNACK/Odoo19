from odoo import models,api

class MachineTransferWizardReport(models.AbstractModel):
    _name = 'report.machine_management.transfer_report_template'
    _description = 'Machine Transfer Wizard Report'

    @api.model
    def _get_report_values(self,docids,data=None):
        transfer_ids = data.get('transfer_ids', []) if data else []
        print(transfer_ids)
        transfer= {self.env['machine.machine.transfer'].browse(docids)}
        print(transfer)
        return {
            'doc_ids': transfer_ids,
            'doc_model': 'machine.machine.transfer',
            'docs': transfer,
            'customer_id': data.get('res_partner_id') ,
            'machine_name_id': data.get('machine_machine_id'),
            'transfer_type':data.get('transfer_type'),
            'transfer_date': data.get('transfer_date'),
            'machine_name':data.get('machine_name'),
            }

