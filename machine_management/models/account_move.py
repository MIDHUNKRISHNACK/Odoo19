from odoo import fields,models,api

class AccountMove(models.Model):
    _inherit ='account.move'

    machine_id=fields.Many2one("machine.machine", string="Machine")
    consumed_parts_ids = fields.One2many('machine.machine.products', string="Parts", compute="_consumed_parts")


    @api.depends('machine_id')
    def _consumed_parts(self):
         for rec in self:
            print(rec.machine_id.product_ids)
            parts = rec.machine_id.product_ids
            self.update({
                  'consumed_parts_ids': [(fields.Command.set(parts.ids))]
                })
