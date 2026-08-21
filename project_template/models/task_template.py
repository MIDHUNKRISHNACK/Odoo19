from odoo import api, fields, models
class TaskTemplate(models.Model):
    _name = 'task.template'


    name = fields.Char(string='Title', tracking=True, required=True, index='trigram')
    description = fields.Html(string='Description', sanitize_attributes=False)
    priority = fields.Selection([
        ('0', 'Low priority'),
        ('1', 'Medium priority'),
        ('2', 'High priority'),
        ('3', 'Urgent'),
    ], default='0', index=True, string="Priority", tracking=True)

    stage_id = fields.Many2one('project.task.type', string='Stage')
    tag_ids = fields.Many2many('project.tags', string='Tags')

    is_ribbon_template=fields.Boolean(string="Is Ribbon", default=True)
    create_date = fields.Datetime("Created On", readonly=True, index=True)
    date_end = fields.Datetime(string='Ending Date', index=True, copy=False)
    date_assign = fields.Datetime(string='Assigning Date', copy=False, readonly=True,
                                  help="Date on which this task was last assigned (or unassigned). Based on this, you can get statistics on the time it usually takes to assign tasks.")
    date_deadline = fields.Datetime(string='Deadline', index=True, tracking=True, copy=False)


    allocated_hours = fields.Float("Allocated Time", tracking=True)

    project_template_id = fields.Many2one('project.template')


    parent_id = fields.Many2one('task.template', string='Parent Task', index=True)
    child_ids = fields.One2many('task.template', 'parent_id', string="Sub-tasks")
    # project_requirement_wizard_id=fields.Many2one('project.requirement.wizard',string='Project Requirement Wizard')




    def button_task_create(self):
        print("task create")




