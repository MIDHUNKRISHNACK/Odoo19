from odoo import models,api,fields

class MachineTransferWizardReport(models.AbstractModel):
    _name = 'report.machine_management.transfer_report_template'
    _description = 'Machine Transfer Wizard Report'


    @api.model
    def _get_report_values(self,docids,data=None):
        """Function for getting values from transiant model and return to the qweb template after checking the customer name of every transfer is same """
        transfer_ids=data.get('transfer_data', []) if data else []
        print(transfer_ids)
        transfer_ids_len=len(transfer_ids)-1
        print(transfer_ids_len)
        list_name=[]
        cus_name=transfer_ids[0]["name"]
        print("cus_name",cus_name)

        for transfer in transfer_ids:
            print(transfer)
            if len(transfer)==4:
                if transfer["name"] not in list_name:
                    list_name.append(transfer["name"])

        print(list_name)
        if len(list_name)==1:
            print("len(list_name)",len(list_name))
            self.write({'is_unique_name':True})
            return {
                'data': transfer_ids,
                'len_transfer_ids': transfer_ids_len,
                'is_unique_name': True,
                'cus_name':list_name[0],
            }

        return {
            'data': transfer_ids,
            'len_transfer_ids': transfer_ids_len,
            'is_unique_name': False,

        }




