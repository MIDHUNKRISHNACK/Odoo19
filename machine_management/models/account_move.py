from odoo import fields,models,api

class AccountMove(models.Model):
    _inherit ='account.move'


    machine_service_id=fields.Many2one('machine.machine.service',string="Machine Service")


    def action_post(self):
      res=super().action_post()
      print("result=", self.machine_service_id)
      self.machine_service_id.write({'is_ribbon_draft':True})
      print("result=",(self.machine_service_id.is_ribbon_draft))
      return res


    def action_create_payments(self):
        res=super().action_register_payment()
        self.machine_service_id.write({'is_ribbon_paid':True})
        print("result2=",(self.machine_service_id.is_ribbon_paid))
        return res
