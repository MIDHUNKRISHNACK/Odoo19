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

    task_ids=fields.One2many('project.task', 'project_template_id', string='Tasks')

    # tasks = fields.One2many('project.task', 'project_id', string="Task Activities")
    #
    # task_ids = fields.One2many('project.task', 'project_id', string='Tasks', export_string_translation=False,domain="[('is_closed', '=', False)]")

    # date_start = fields.Date(string='Start Date', copy=False)
    # date = fields.Date(string='Expiration Date', copy=False, index=True, tracking=True,
    #                    help="Date on which this project ends. The timeframe defined on the project is taken into account when viewing its planning.")
    # allow_task_dependencies = fields.Boolean('Task Dependencies', inverse='_inverse_allow_task_dependencies')
    # allow_milestones = fields.Boolean('Milestones', inverse='_inverse_allow_milestones')
    # allow_recurring_tasks = fields.Boolean('Recurring Tasks', inverse='_inverse_allow_recurring_tasks')
    # tag_ids = fields.Many2many('project.tags', relation='project_project_project_tags_rel', string='Tags')





