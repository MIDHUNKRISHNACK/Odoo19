from odoo import fields,models,api

class AccountMove(models.Model):
    _inherit ='account.move'


    machine_service_id=fields.Many2one('machine.machine.service',string="Machine Service")
    ribbon_paid=fields.Boolean(string="Ribon Paid",compute="_compute_ribbon_paid")


    def action_post(self):
      """Function to execute draft ribbon when posting to the machine service invoice"""
      res=super().action_post()
      print("result=", self.machine_service_id)
      self.machine_service_id.write({'is_ribbon_draft':True})
      print("result=",(self.machine_service_id.is_ribbon_draft))
      return res

    def action_register_payment(self):
        """Function to execute post ribbon when posting to the machine service invoice"""
        res=super().action_register_payment()
        self.machine_service_id.write({'is_ribbon_post':True})
        print("result2=",(self.machine_service_id.is_ribbon_post))
        return res






