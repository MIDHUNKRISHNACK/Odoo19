
from odoo import fields,models,api
from odoo.orm.commands import Command
from odoo.orm.models import BaseModel


class Saleorder(models.Model):
    _inherit ='sale.order'


    sale_order_project_id= fields.Integer(string="Project ID")


    def button_task_create(self):
        """Function for creating a Project and subtasks from an sale order line. customer name is the project name and milestone value is the main task name then related products are the subtasks"""

        project_milestone=self.env['project.project'].create({
            'name': self.partner_id.name,
        })
        milestone_task = self.order_line.mapped(lambda orderline: orderline.milestone)
        print(milestone_task)
        milestone_tasks=[]
        mile_stone_count = 0
        for milestone in milestone_task:
            sub_task = []
            orderline_filter = self.order_line.filtered(lambda rec: rec.milestone == mile_stone_count)
            if orderline_filter:
                print(orderline_filter)
                for rec in orderline_filter:
                    sub_task.append(Command.create({
                        'name': rec.product_template_id.name,
                        'project_id':project_milestone.id,

                    }))
                print(sub_task)
                milestone_tasks.append(Command.create({
                        'name': "Milestone" + " " + str(mile_stone_count),
                        'project_id': project_milestone.id,
                        'child_ids': sub_task,

                    }))
                print(milestone_task)
                print(sub_task)

            mile_stone_count += 1
            continue
        self.sale_order_project_id=project_milestone.id
        project_milestone.update({
            'task_ids': milestone_tasks,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'sale_order_project_redirect',
            'res_model': 'project.project',
            'res_id': self.sale_order_project_id,
            'view_mode': 'kanban,list,form',
            'target': 'self',


        }

    def action_open_project_view(self):
        """ Function for opening project view of sale order in smart button """
        return {
            'type': 'ir.actions.act_window',
            'name': 'sale_order_task_redirect',
            'res_model': 'project.project',
            'res_id': self.sale_order_project_id,
            'view_mode': 'form',
            'target': 'self',
        }


