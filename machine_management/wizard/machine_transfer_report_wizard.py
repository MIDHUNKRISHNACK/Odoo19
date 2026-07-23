import io
import json
from datetime import datetime, date
from dateutil.rrule import rrule, DAILY
from odoo import fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import date_utils, json_default
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class MachineTransferReportWizard(models.TransientModel):
    _name = "machine.transfer.report.wizard"
    _description = "Machine Transfer Report Wizard"
    from_date = fields.Datetime(string="From Date",required=True)
    to_date = fields.Datetime(string="To Date",required=True)
    transfer_type=fields.Selection([('install','Install'),('remove','Remove')],string="Transfer Type")
    customer_ids=fields.Many2many(string="Customer Name",comodel_name="res.partner")
    machine_name_ids=fields.Many2many(string="Machine Name",comodel_name="machine.machine")

    def action_print_machine_transfer_xlsx_report(self):
        data={
            "from_date":self.from_date.date(),
            "to_date":self.to_date.date(),
            "customer_ids":self.customer_ids.ids,
            "machine_name_ids":self.machine_name_ids.ids,
            "transfer_type":self.transfer_type,
        }
        print(data)
        return {
            'type': 'ir.actions.report',
            'data': {'model': 'machine.transfer.report.wizard',
                     'options': json.dumps(data, default=json_default),
                     'output_format': 'xlsx',
                     'report_name': 'Machine Report',
                     },
            'report_type': 'xlsx',
        }

    def get_xlsx_report(self,data, response):
        customer = tuple(data['customer_ids'])
        machine = tuple(data['machine_name_ids'])
        print(customer)
        print(machine)

        query = """SELECT DISTINCT machine_machine.machine_name,machine_machine_transfer.transfer_type,res_partner.name,machine_machine_transfer.transfer_date FROM machine_machine_transfer INNER JOIN machine_machine ON machine_machine_transfer.machine_name_id=machine_machine.id INNER JOIN res_partner ON machine_machine_transfer.customer_name_id=res_partner.id
                WHERE machine_machine_transfer.customer_name_id IN %s AND machine_machine_transfer.machine_name_id IN %s AND machine_machine_transfer.transfer_type='%s' AND machine_machine_transfer.transfer_date>='%s' AND machine_machine_transfer.transfer_date<='%s'""" % (
            customer, machine, data['transfer_type'],data['from_date'],data['to_date'])
        self.env.cr.execute(query)
        transfer_ids = self.env.cr.dictfetchall()

        print(transfer_ids)
        print("length of =", len(transfer_ids))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        sheet.set_column(0,5,30)
        sheet.set_row(11,40)

        border = workbook.add_format({'border': 1})
        head=workbook.add_format({'bold':True,'font_size':30,'align':'center'})
        table_head=workbook.add_format({'bold':True,'font_size':15,'align':'center','border':1})
        date_size=workbook.add_format({'font_size':12,'bold':True,'align':'center'})
        sheet.merge_range('A1:C4','MACHINE TRANSFER REPORT',head)
        sheet.merge_range('A6:A7','From Date = '+data['from_date'],date_size)
        sheet.merge_range('A8:A9','To Date = '+data['to_date'],date_size)
        heading_key=["machine_name","Transfer_type","Customer_Name","Transfer_Date"]

        row=11
        col=0
        for key in heading_key:
            sheet.write(row,col,key,table_head)
            col += 1
        print("a")

        t_row=12
        col=0
        for doc in transfer_ids:
            values = []
            for key in doc:
                if key == 'transfer_date':
                    t_date=doc[key].strftime('%Y-%m-%d')
                    values.append(t_date)
                else:
                 values.append(doc[key])
            sheet.write_row(t_row,col,tuple(values),border)
            t_row+= 1

            # t_col=0
            # values.append(doc["machine_name"])
            # values.append(doc["name"])
            # transfer_date=doc["transfer_date"]
            # print(transfer_date)
            # print(transfer_date.day)
            # values.append(transfer_date)
            # values.append(doc["transfer_type"])
            # tuple_values=tuple(values)
            # print(tuple_values)
            # sheet.write_row(t_row,t_col,tuple_values,border)
            # t_row+=1



        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


    def action_print_machine_transfer_report(self):
        """ Function for filtering values based on the given fields in wizard and passes to the abstract model """
        print(self.env.cr.dbname)
        customer=tuple(self.customer_ids.ids)
        machine=tuple(self.machine_name_ids.ids)
        print(customer)
        print(machine)
        print(self.transfer_type)
        print(self.to_date.date())


        query="""SELECT DISTINCT machine_machine.machine_name,machine_machine_transfer.transfer_type,res_partner.name,machine_machine_transfer.transfer_date FROM machine_machine_transfer INNER JOIN machine_machine ON machine_machine_transfer.machine_name_id=machine_machine.id INNER JOIN res_partner ON machine_machine_transfer.customer_name_id=res_partner.id
        WHERE machine_machine_transfer.customer_name_id IN %s AND machine_machine_transfer.machine_name_id IN %s AND machine_machine_transfer.transfer_type='%s' AND machine_machine_transfer.transfer_date>='%s' AND machine_machine_transfer.transfer_date<='%s'""" %(customer,machine,self.transfer_type,self.from_date.date(),self.to_date.date())
        self.env.cr.execute(query)
        transfer_ids=self.env.cr.dictfetchall()
        transfer_ids.append({
            "from_date":self.from_date.date(),
            "to_date":self.to_date.date()
        })
        print(transfer_ids)
        print("length of =",len(transfer_ids))



        return self.env.ref(
                'machine_management.action_machine_transfer_wizard_report'
            ).report_action(None, data={'transfer_data':transfer_ids})



        # Method for filtering values using Domain
        # domain=[
        #     ('transfer_date', '>=', self.from_date),
        #     ('transfer_date', '<=', self.to_date),
        # ]
        # total_machine_transfers = self.env['machine.machine.transfer'].search(domain)
        # print(total_machine_transfers)
        # if self.machine_name_id:
        #     domain.append(('machine_name_id', '=', self.machine_name_id.id))
        #     domain.append(('customer_name_id','=',self.customer_id.id))
        #
        #     machine_transfers = self.env['machine.machine.transfer'].search(domain)
        #     print(machine_transfers)
        #     data = {
        #         'from_date': str(self.from_date),
        #         'to_date': str(self.to_date),
        #         'customer_id':self.customer_id.name,
        #         'machine_name_id':self.machine_name_id.machine_name,
        #         'transfer_ids':machine_transfers.ids,
        #     }
        #
        #     print(self.customer_id.name)
        #     print(self.machine_name_id.machine_name)
        #     print(machine_transfers.ids)
        #     return self.env.ref(
        #         'machine_management.action_machine_transfer_wizard_report'
        #     ).report_action(None, data=data)
