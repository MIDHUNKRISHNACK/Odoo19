from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit='res.partner'

    machine_count=fields.Integer(compute='_compute_count',string='Number of Machines')
    machine_ids=fields.One2many('machine.machine','customer_name_id',string='Machines')


    def action_archive(self):
        """Function to archive the machine list related to this partner"""
        res=super().action_archive()
        print("returned machine list =", self.machine_ids)
        print("returned machine list =", self.machine_ids.ids)
        for rec in self:
         machine=rec.machine_ids
         print("machine_name=",machine)
         machine.action_archive()
        return res


    def action_unarchive(self):
        """Function to unarchive the machine list related to this partner"""
        res = super().action_unarchive()
        for rec in self:
            machine = rec.with_context(active_test=False).machine_ids
            print("machine_name_unarchive=",machine)
            machine.action_unarchive()
        return res


    def _compute_count(self):
        """Function to calculate the number of machines related to this partner"""
        for rec in self:
            machine_count = rec.env["machine.machine"].search_count([
                ('customer_name_id','=',rec.id)
            ])
            rec.machine_count = machine_count


    def action_open_machine_list_view(self):
        """action for opening machine list view"""
        return {
           'type': 'ir.actions.act_window',
           'name': 'machine_list_redirect',
           'res_model': 'machine.machine',
           'domain':[('customer_name_id', '=', self.id)],
           'view_mode': 'list,form',
           'target': 'self',
        }

