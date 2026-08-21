from odoo import api, fields, models, tools
class ProjectTemplate(models.Model):
    _name = 'project.template'

    project_template_id=fields.Many2one('project.project')
    name = fields.Char("Name", index='trigram', required=True, tracking=True, translate=True,
                       default_export_compatible=True)
    description = fields.Html(help="Description to provide more information and context about this project")
    partner_id = fields.Many2one('res.partner', string='Customer', bypass_search_access=True, tracking=True,
                                 domain="['|', ('company_id', '=?', company_id), ('company_id', '=', False)]",
                                 index='btree_not_null')
    company_id = fields.Many2one('res.company', string="Company", default=lambda self: self.env.user.company_id.id)

    task_ids=fields.One2many('task.template', 'project_template_id', string='Tasks')
    is_ribbon_template=fields.Boolean(string="Is Ribbon", default=True)
    task_count=fields.Integer(string="Task Count",compute="_compute_task_count",store=True)

    def _compute_task_count(self):
        self.task_count = len(self.task_ids)


    def button_project_create(self):
        print("project")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create New Project',
            'res_model': 'project.requirement.wizard',
            'context': {
                'default_project_template_id': self.id,
                'default_company_id': self.company_id.id,
                'default_task_ids': self.task_ids.ids,
            },
            'view_mode': 'form',
            'target': 'new',
        }


    def action_open_project_list(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'open_task_list',
            'res_model':'task.template',
            'domain': [("id", "in", self.task_ids.ids)],
            'view_mode': 'list,form',
            'target': 'self',
        }







