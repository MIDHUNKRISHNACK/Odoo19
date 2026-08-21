from odoo import fields, models, api
class ProjectProject(models.Model):
    _inherit = "project.project"


    def button_project_template_create(self):
        task_ids=[]
        child_ids=[]
        print(len(self.task_ids))
        for rec in self.task_ids:
         for task in rec.child_ids:
            child_ids.append(fields.Command.create({
                'name': task.name,
                'create_date': task.create_date,
                'date_end': task.date_end,
                'allocated_hours': task.allocated_hours,
            }))
        for rec in self.task_ids:

          taskid=self.env["task.template"].create({
                    'name':rec.name,
                    'create_date':rec.create_date,
                    'date_end':rec.date_end,
                    'tag_ids':[fields.Command.set(rec.tag_ids.ids)],
                    'allocated_hours':rec.allocated_hours,
                    'child_ids':child_ids,

                })
          task_ids.append(taskid.id)
          print(task_ids)

        rec=self.env["project.template"].create({
                'project_template_id': self.id,
                'name':self.name,
                'description':self.description,
                'partner_id':self.partner_id.id,
                'task_ids':task_ids,

            })
        print(rec)

