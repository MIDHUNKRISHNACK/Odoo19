from odoo import api, fields, models, tools
from odoo.orm.decorators import readonly


class ProjectRequirementWizard(models.TransientModel):
    _name = 'project.requirement.wizard'

    project_template_id = fields.Many2one('project.template',readonly=True)
    user_id = fields.Many2one('res.users')
    date_start=fields.Datetime(string='Start Date')
    allocated_hours = fields.Float(string='Allocated Hours')
    company_id = fields.Many2one('res.company',readonly=True)

    def action_create_project(self):
        print("neww")
        print(self.project_template_id.name)
        print(self.company_id.id)
        print(self.user_id.id)
        print(self.date_start)
        print(self.allocated_hours)
        project_id=self.env['project.project'].create({
            'name': self.project_template_id.name,
            'label_tasks':"Tasks",
            'company_id': self.company_id.id,
            'user_id': self.user_id.id,
            'date_start': self.date_start,

        })
        print(project_id)
        print(project_id)
        task_ids=[]
        child_ids=[]
        for rec in self.project_template_id.task_ids:
            for task in rec.child_ids:
              child_ids.append(fields.Command.create({
                    'project_id': project_id.id,
                    'name': task.name,
                    'create_date': task.create_date,
                    'date_end': task.date_end,
                    'allocated_hours': task.allocated_hours,
                }))

            taskid = self.env["project.task"].create({
                'project_id': project_id.id,
                'name': rec.name,
                'create_date': rec.create_date,
                'date_end': rec.date_end,
                'tag_ids': [fields.Command.set(rec.tag_ids.ids)],
                'allocated_hours': rec.allocated_hours,
                'child_ids': child_ids,

            })
            task_ids.append(taskid.id)
            print(task_ids)

        project_id.update({'task_ids': task_ids})









