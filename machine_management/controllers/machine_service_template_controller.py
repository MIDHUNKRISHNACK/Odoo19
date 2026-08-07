from pickle import GET

from reportlab.graphics.transform import inverse

from odoo import http
from odoo.http import request

class MachineServiceTemplateController(http.Controller):
    @http.route('/newuser-odoo', type='http', auth='public', website=True)
    def create_new_customer(self, **post):
        """Function for rendering new customer creation form template"""
        return request.render('machine_management.new_user_registration')


    @http.route('/customer-create', type='http', auth='public', website=True,methods=['POST'],csrf=True)
    def create_new_user(self, **post):
        """Function for getting new user details from template and create new record in res.partner then renders a thnk you page"""
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
        """Function for rendering service details form template"""
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
            'machine_type_ids':machine_type_ids,

        })

    @http.route(['/service-create'], type='http', auth="public", methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        """Function for creating new record in machine service model"""
        print("hiihiii")
        print("self =",self)
        print("request =",request)
        print("post =",post)
        print("customer =",post.get('customer_id'))
        print("machine_name =",post.get('machine_name'))
        print("purchase_date =",post.get('purchase_date'))

        request.env['machine.machine.service'].sudo().create({
            'customer_id': post.get('cus_name'),
            'machine_id': post.get('machine_name'),
            'date_of_service': post.get('purchase_date'),

        })
        return request.render('website.contactus_thanks')

    @http.route('/my/machines',type='http', auth='public', website=True)
    def machine_list(self, **post):
        """Function for passing the machine record set to the portal template"""
        machine_ids=request.env['machine.machine'].sudo().search([])

        return request.render('machine_management.portal_machine',{
            'machine_ids': machine_ids,
        })

    @http.route('/machines/form',type='http', auth='public', website=True,methods=['GET'],csrf=True)
    def machine_form(self, **post):
        """Function for passing the specific machine record and url for redirection to the basic template"""
        print("hello")
        print(GET)
        print(post)
        print(list(post.keys()))
        machine=list(post.keys())
        print(machine[0])
        machine_id=self.env['machine.machine'].search([('id','=',machine[0])])
        print(machine_id)
        machine_ref=self.env.ref('machine_management.machine_mangt_actions')
        print(machine_ref.id)
        link="/odoo/action-"+str(machine_ref.id)+"/"+str(machine[0])
        print("link",link)

        return request.render('machine_management.machines_form',{
            'machine_id':machine_id,
            'link':link,

        })

    @http.route('/get_top_machine_list',auth='public', type='jsonrpc', website=True)
    def get_top_machine_list(self, **post):
     print(self)
     print("World")
     machine_ids=request.env['machine.machine'].sudo().search([], order='serial_number desc')
     print(machine_ids)

     machine_list=[]
     for rec in machine_ids:
         machine_list.append({
             'id': rec.id,
             'serial_number': rec.serial_number,
             'machine_name': rec.machine_name,
             'purchase_date': rec.date_of_purchase,
             'purchase_value': rec.purchase_value,
             'machine_image':'/web/image/machine.machine/%s/image'%rec.id,
             'status': rec.status,
         })

     return machine_list

    @http.route('/customer-create', type='jsonrpc', auth='public', website=True)
    def create_new_user(self, **post):
        """Function for getting new user details from template and create new record in res.partner then renders a thnk you page"""
        print(post)

        if post.get('type') == 'person':
            request.env['res.partner'].sudo().create({
                'company_type': 'person',
                'name': post.get('name'),
                'email': post.get('email'),

            })
        else:
            request.env['res.partner'].sudo().create({
                'company_type': 'company',
                'name': post.get('name'),
                'email': post.get('email'),

            })














