from odoo import fields, models, api
class ProjectProject(models.Model):
    _inherit = "project.project"


    def button_project_template_create(self):


        task_ids=[]
        for rec in self.task_ids:
            task_ids.append(fields.Command.create({
                'id':rec.id,
            }))

        rec=self.env["project.template"].create({
            'project_template_id': self.id,
            'name':self.name,
            'description':self.description,
            'partner_id':self.partner_id.id,
            'task_ids':task_ids,

        })
        print(rec)

