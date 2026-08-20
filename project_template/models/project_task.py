from odoo import api, fields, models
class ProjectTask(models.Model):
    _inherit = 'project.task'

    project_template_id = fields.Many2one('project.template',string='Project Template id')
