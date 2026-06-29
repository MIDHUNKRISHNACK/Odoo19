from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit='res.partner'


    def action_open_machine_list_view(self):

        return {
           'type': 'ir.actions.act_window',
           'name': 'machine_list_redirect',
           'res_model': 'machine.machine',
           'domain':[('customer_name_id', '=', self.id)],
           'view_mode': 'list',
           'target': 'self',
        }