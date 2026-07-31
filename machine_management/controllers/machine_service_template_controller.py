from odoo import http
from odoo.http import request

class MachineServiceTemplateController(http.Controller):
    @http.route('/newuser-odoo', type='http', auth='public', website=True)
    def create_new_customer(self, **post):
        return request.render('machine_management.new_user_registration')


    @http.route('/customer-create', type='http', auth='public', website=True,methods=['POST'],csrf=True)
    def create_new_user(self, **post):
        if post.get('user_type')=='person':
            request.env['res.partner'].sudo().create({
                'company_type':'person',
                'name': post.get('name'),
                'phone': post.get('phone_number'),
                'email': post.get('email'),
                'street': post.get('address')
                          })
        else:
            request.env['res.partner'].sudo().create({
                'company_type': 'company',
                'name': post.get('name'),
                'phone': post.get('phone_number'),
                'email': post.get('email'),
                'street': post.get('address')
            })

        return request.render('website.contactus_thanks')

    @http.route(['/thanks'], type='http', auth="public", methods=['GET'], website=True)
    def service_list(self, **post):
        return request.redirect('/contactus-thank-you')

    @http.route('/service-odoo', type='http', auth='public', website=True)
    def machine_service(self, **kwargs):
        print(self)
        customer_ids=request.env['res.partner'].sudo().search([])
        machine_ids=request.env['machine.machine'].sudo().search([])
        machine_type_ids=request.env['machine.machine.types'].sudo().search([])
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        print(user_name)

        return request.render('machine_management.machine_machine_service_template', {
            'user_name': user_name,
            'customer_ids': customer_ids,
            'machine_ids': machine_ids,
            'machine_type_ids':machine_type_ids
        })

    @http.route(['/service-create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        print("hiihiii")
        print("self =",self)
        print("request =",request)
        print("post =",post)
        print("customer =",post.get('customer_id'))
        print("machine_name =",post.get('machine_name'))
        print("purchase_date =",post.get('purchase_date'))
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
        # return request.render('website.contactus_thanks')



