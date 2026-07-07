from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
import datetime

class machine_machine(models.Model):
    _name = 'machine.machine'
    _description = 'Machine List'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'machine_name'

    customer_name_id=fields.Many2one('res.partner',string="Customer Name",readonly=True)
    date_of_purchase=fields.Date(string="Date Of Purchase",required=True,help="Enter the date of purchase")
    quantity=fields.Integer(string="Quantity",required=True,help="Enter the quantity of purchase")
    company_id = fields.Many2one('res.company', store=True, copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related="company_id.currency_id")
    purchase_value = fields.Monetary(string="Purchase Value")
    machine_name= fields.Char( required=True,help="Enter the name of the machine",tracking=True)
    description=fields.Char(string="Description",required=True,help="Enter the description of the machine")
    is_warrenty=fields.Boolean(string="warrenty",help="Warrenty status",default=False)
    status=fields.Selection([('active','Active'),('inservice','Inservice')],default='active',tracking=True,help="Select the status of machine")
    image=fields.Image(required=True)
    instructions=fields.Html(string="Instructions")
    machine_ref=fields.Char(readonly=True,default=_("New"))
    machine_type_id=fields.Many2one('machine.machine.types',string="Machine Type")
    serial_number=fields.Char(string="Serial Number")
    transfer_count=fields.Integer(string="Transfer Count",compute="_compute_transfer_count")
    is_button_sts=fields.Boolean(default=False)
    machine_tag_ids=fields.Many2many('machine.machine.tags',string="Machine Tags")
    product_ids=fields.One2many('machine.machine.products','model_name_id',string="Machine Products",store=True)
    case_count=fields.Integer(string="Case Count",compute="_compute_case_count")
    machine_age=fields.Integer(string="Machine Age",compute="_compute_machine_age",readonly=True)
    active=fields.Boolean('Is Active' ,default=True)
    demo_data=fields.Boolean('Demo Data',invisible=True,default=True)
    machine_transfer_ids=fields.One2many('machine.machine.transfer','machine_name_id',string="transfer list")
    machine_service_ids=fields.One2many('machine.machine.service','machine_id',string='case list')
    service_frequency = fields.Selection([('weekly', 'Weekly'), ('monthly', 'Monthly'), ('yearly', 'YEARLY')],string="Service Frequency")
    next_service_date= fields.Date(string="Next Service Date",compute="_compute_next_service_date")




    @api.depends('service_frequency')
    def _compute_next_service_date(self):
        if self.service_frequency == 'weekly':
            self.next_service_date= self.date_of_purchase + datetime.timedelta(weeks=1)
        elif self.service_frequency == 'monthly':
            self.next_service_date= self.date_of_purchase + datetime.timedelta(30)
        elif self.service_frequency == 'yearly':
            self.next_service_date= self.date_of_purchase + datetime.timedelta(365)
        else:
            self.next_service_date= self.date_of_purchase




    def action_cron_test_method(self):
          date_now=fields.Date.today()
          machine_list = self.env['machine.machine'].search([('status','=','inservice')])

          print(date_now)
          print("total machine list",machine_list)
          for rec in machine_list:
            service_list=rec.machine_service_ids.search([('service_state','!=','open')])
            len_service_list=len(service_list)
            if len_service_list==0:
                self.env['machine.machine.service'].create({
                    'machine_id': rec.id,
                    # 'date_of_service': rec.next_service_date
                })













    #     machine_list = self.env['machine.machine.service'].search([])
    #     # print('value of self=', self)
        # machine_name = self.env['machine.machine'].search([])
        #
        # sorted_list = machine_name.sorted(lambda record: record.status=='inservice', reverse=True)
        # record_id = sorted_list[0]
        # service_list =record_id.machine_service_ids.search_count([('service_state', '=', 'open')])
        # print('rec=', record_id)
        # print('recids',record_id.machine_service_ids)
        # print(machine_name)
        # print(sorted_list)
        # if self.service_frequency=='weekly':
        #
        #     self.write({
        #         'next_service_date': record_id.date_of_purchase + datetime.timedelta(7),
        #     })
        #     print('value of next date=', record_id.next_service_date)
        # elif self.service_frequency=='monthly':
        #
        #     self.write({
        #         'next_service_date': record_id.date_of_purchase + datetime.timedelta(30),
        #     })
        #     print('value of next date=', record_id.next_service_date)
        # else:
        #     self.write({
        #         'next_service_date': record_id.date_of_purchase,
        #     })
        #
        #
        # print('name=',record_id.machine_name)
        # print("next date=", record_id.next_service_date)
        # print("service_list",service_list)
        # print("state=",record_id.status)
        # print("state value=",record_id.status=='inservice')
        #
        # if service_list==0 and record_id.status=='inservice':
        #      self.env['machine.machine.service'].create({
        #         'machine_id':record_id.id,
        #         'date_of_service':record_id.next_service_date,
        #      })







    def action_archive(self):
        """Function to archive the machine list related to this partner"""
        open_case=self.machine_service_ids.search_count([('service_state', '=', 'open')])
        print("service_list",self.machine_service_ids)
        print("opencase_count",open_case)
        if self.status=='inservice' and open_case==0 :
         res = super().action_archive()
         print("returned machine list =", self.machine_transfer_ids)
         print("returned machine list =", self.machine_transfer_ids.ids)
         for rec in self:
            machine_list = rec.machine_transfer_ids
            machine_list.action_archive()
        else:
           return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'type': 'danger',
                    'sticky': False,
                    'message': _("Already One case is Open Stage!"),
                     'next': self.change_case_state(),
                }
            }


        return res

    def change_case_state(self):
        self.machine_service_ids.write({
            'service_state':'cancel'
        })


    @api.depends('date_of_purchase')
    def _compute_machine_age(self):
        """Function to calculate machine age"""
        current_date=fields.Date.today()
        print(current_date)
        for rec in self:
         purchase=rec.date_of_purchase
         print(type(current_date))
         print(type(purchase))
         print("Purcggvbeghyte",purchase)

         if purchase:
            rec.machine_age=(current_date-purchase).days
            print('machine_age_old=',(current_date-purchase))
            print('machine_age=',rec.machine_age)
         else:
            rec.machine_age=0
            print('machine_age=', rec.machine_age)


    # @api.ondelete(at_uninstall=True)
    # def _check_before_delete(self):
    #     for rec in self:
    #         if rec.is_button_sts == True:
    #             raise ValidationError("Machine is still in Transfer state ")



    # def unlink(self):
    #     for rec in self:
    #         if rec.is_button_sts == True:
    #             raise ValidationError("Machine is still in Transfer state ")
    #     return super().unlink()



     # sql constraints
    _serial_number_unique = models.Constraint(
        'unique(serial_number)',
        'The serial number of the machine is already exist give another .',
    )


    def _compute_transfer_count(self):
        """ Function to calculate transfer count of machine """
        for rec in self:
           transfer_count= self.env["machine.machine.transfer"].search_count([
                 ('machine_name_id', '=', rec.id)

             ])
           if transfer_count >=1:
                rec.is_button_sts=True

           rec.transfer_count =transfer_count


    def _compute_case_count(self):
        """ Function to calculate case count of machine """
        for rec in self:
            case_count=self.env["machine.machine.service"].search_count([
                ('machine_id', '=', rec.id)
            ])
            if case_count >=1:
                rec.is_button_sts=True

            rec.case_count=case_count


    @api.constrains('purchase_value')
    def _check_purchase_value(self):
        """ Function to validate purchase value , less than or equal to zero"""
        for record in self:
            if record.purchase_value <=0:
                raise ValidationError("Purchase value must be greater than 0")



    def button_transfer_redirect(self):
        """Function to Redirect to machine transfer list while clicking button transfer """
        return {
                     'type': 'ir.actions.act_window',
                     'name':'machine_transfer_redirect',
                     'res_model': 'machine.machine.transfer',
                     'view_mode': 'form',
                     'target': 'self',
                     'context': {'default_machine_name_id': self.id},

                }


    @api.model_create_multi
    def create(self, vals_list):
        """ Function to create Sequence Number for each machines """
        for vals in vals_list:
            if vals.get('machine_ref', _("New")) == _("New"):

                vals['machine_ref'] = self.env['ir.sequence'].next_by_code('m_seq')

        return super(machine_machine,self).create(vals_list)



    def action_open_machine_list(self):
        """ Function to redirect to specific machine transfer list by clicking smart button """
        return {
           'type': 'ir.actions.act_window',
           'name': 'machine_transfer_redirect',
           'res_model': 'machine.machine.transfer',
           'domain':[('machine_name_id', '=', self.id)],
           'view_mode': 'list,form',
           'target': 'self',
    }

    def action_open_case_list(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'machine_service_list',
            'res_model': 'machine.machine.service',
            'domain': [('machine_id', '=', self.id)],
            'view_mode': 'list',
            'target': 'self',
            }


    def button_service_redirect(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'machine_service_redirect',
            'res_model': 'machine.machine.service',
            'view_mode': 'form',
            'target': 'self',
            'context': {'default_machine_id': self.id,
                        'default_customer_id':self.customer_name_id.id
                        },
        }





