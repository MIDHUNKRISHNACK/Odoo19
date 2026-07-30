from odoo import http
from odoo.http import request

class MachineServiceTemplateController(http.Controller):
    @http.route('/service-odoo', type='http', auth='public', website=True)
    def machine_service(self, **kwargs):
        print(self)
        customer_ids=request.env['res.partner'].sudo().search([])
        machine_ids=request.env['machine.machine'].sudo().search([])
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        return request.render('machine_management.machine_machine_service_template', {
            'user_name': user_name,
            'customer_ids': customer_ids,
            'machine_ids': machine_ids,
        })

    @http.route(['/service-create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        print("self =",self)
        print("request =",request)
        print("post =",post)
        # cus_name=request.env['res.partner'].sudo().create({
        #     'name': post.get('cus_name'),
        #
        # })
        # machine_name=request.env['machine.machine'].sudo().create({
        #     'machine_name': post.get('name'),
        #     'quantity': post.get('quantity'),
        #
        #
        # })
        request.env['machine.machine.service'].sudo().create({
            'customer_id': post.get('cus_name'),
            'machine_id': post.get('machine_name'),
            'date_of_service': post.get('purchase_date'),

        })
        return request.render('machine_management.service_register_success_template')
