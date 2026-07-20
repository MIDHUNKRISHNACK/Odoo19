from odoo import models,api


class Machine_Transfer_Wizard_Report(models.AbstractModel):
    _name = 'report.machine_management.transfer.report.template'
    _description = 'Machine Transfer Wizard Report'

    @api.model
    def _get_report_values(self,docids,data=None):
        transfer_ids = data.get('transfer_ids', []) if data else []
        print(transfer_ids)
        transfer= self.env['machine.machine.transfer'].browse(transfer_ids)
        print(transfer)
        return {
            'doc_ids': transfer_ids,
            'doc_model': 'machine.machine.transfer',
            'docs': transfer,
            'from_date': data.get('from_date', '') if data else '',
            'to_date': data.get('to_date', '') if data else '',
            'customer_id': data.get('customer_id') ,
            'machine_name_id': data.get('machine_name_id'),
            }

