from odoo import fields, models,api,_
from odoo.exceptions import UserError


class ProjectTask(models.Model):
    _inherit = 'project.task'

    hours_limit = fields.Float(string="Hours Per day",default=0)


    @api.onchange('timesheet_ids','hours_limit')
    def _onchange_timesheet_ids(self):
        """Function for showing the user error while the timesheet of perticular day reaches the time limit per day """
        date_list = {}
        for rec in self.timesheet_ids:
            date=rec.date
            print('now',date_list)
            print(date)
            if date in date_list:
                time_spend=(date_list[rec.date]+rec.unit_amount)
                print(time_spend)
                if time_spend>self.hours_limit: raise UserError(_("hours limit reaches the %s hr of %s.The total Worked hours of the day %s is %s",self.hours_limit,rec.date,rec.date,time_spend))
                date_list.update({rec.date: time_spend})
                print("Updated List",date_list)

            else:
                date_list.update({rec.date: rec.unit_amount})
                print("newly created",date_list)
                time_spend=rec.unit_amount

                if time_spend>self.hours_limit:
                    raise UserError(_("hours limit reaches the %s hr of %s.The total Worked hours of the day %s is %s",self.hours_limit,rec.date,rec.date,date_list[rec.date]))



