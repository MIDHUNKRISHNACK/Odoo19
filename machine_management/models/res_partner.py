from odoo import fields,models,api

class ResPartner(models.Model):
    _inherit='res.partner'

    machine_id=fields.Many2one('machine.machine',string='Machine name')
    machine_count=fields.Integer(compute='_compute_count',string='Number of Machines')

    # def action_archive(self):
    #     res=super().action_archive()
    #     if self.active :
    #         self.machine_id.write({'active':True})
    #     else:
    #         self.machine_id.write({'active':False})
    #     return res
    #


    def _compute_count(self):
        for rec in self:
            machine_count = rec.env["machine.machine"].search_count([
                ('customer_name_id','=',rec.id)
            ])
            rec.machine_count = machine_count

    def action_open_machine_list_view(self):

        return {
           'type': 'ir.actions.act_window',
           'name': 'machine_list_redirect',
           'res_model': 'machine.machine',
           'domain':[('customer_name_id', '=', self.id)],
           'view_mode': 'list',
           'target': 'self',
        }

