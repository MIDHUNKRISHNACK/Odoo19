import io
from odoo import fields, models, _
from odoo.exceptions import ValidationError
try:
    from odoo.tools.misc import xlsxwriter
except ImportError:
    import xlsxwriter

class machine_transfer_wizard_xlsx_report(models.AbstractModel):
    _name = 'machine.transfer.wizard.xlsx'


    def get_xlsx_report(self, data, response):
        """Function for designing and creating xlsx report based on the given field values """
        where = []
        param = []
        if data['from_date']:
            where.append("machine_machine_transfer.transfer_date >= %s")
            param.append(data['from_date'])
        if data['to_date']:
            where.append("machine_machine_transfer.transfer_date <= %s")
            param.append(data['to_date'])

        db_query = """SELECT DISTINCT machine_machine.machine_name,machine_machine_transfer.transfer_type,res_partner.name,machine_machine_transfer.transfer_date FROM machine_machine_transfer INNER JOIN machine_machine ON machine_machine_transfer.machine_name_id=machine_machine.id INNER JOIN res_partner ON machine_machine_transfer.customer_name_id=res_partner.id """

        if where:
            print(where)
            db_query += " WHERE " + " AND ".join(where)

        self.env.cr.execute(db_query, tuple(param))
        transfer_ids = self.env.cr.dictfetchall()

        if len(transfer_ids) == 0:
            raise ValidationError(f"No Transfer was found In Between {data['from_date']} and {data['to_date']}")

        print(data['customer_ids'])
        print(data['machine_name_ids'])
        print(data['transfer_type'])
        print(data['from_date'])
        print(data['to_date'])
        where = []
        param = []
        if data['customer_ids']:
            if len(data['customer_ids']) == 1:
                where.append("machine_machine_transfer.customer_name_id = %s")
                param.append(tuple(data['customer_ids'], ))
            else:
                where.append("machine_machine_transfer.customer_name_id IN %s")
                param.append(tuple(data['customer_ids']))
        if data['machine_name_ids']:
            if len(data['machine_name_ids']) == 1:
                where.append("machine_machine_transfer.machine_name_id = %s")
                param.append(tuple(data['machine_name_ids'], ))
            else:
                where.append("machine_machine_transfer.machine_name_id IN %s")
                param.append(tuple(data['machine_name_ids']))
        if data['transfer_type']:
            where.append("machine_machine_transfer.transfer_type = %s")
            param.append(data['transfer_type'])
        if data['from_date']:
            where.append("machine_machine_transfer.transfer_date >= %s")
            param.append(data['from_date'])
        if data['to_date']:
            where.append("machine_machine_transfer.transfer_date <= %s")
            param.append(data['to_date'])

        query = """SELECT DISTINCT machine_machine.machine_name,machine_machine_transfer.transfer_type,res_partner.name,machine_machine_transfer.transfer_date FROM machine_machine_transfer INNER JOIN machine_machine ON machine_machine_transfer.machine_name_id=machine_machine.id INNER JOIN res_partner ON machine_machine_transfer.customer_name_id=res_partner.id """

        if where:
            print(where)
            query += " WHERE " + " AND ".join(where)

        self.env.cr.execute(query, tuple(param))
        transfer_ids = self.env.cr.dictfetchall()

        if len(transfer_ids) == 0:
            raise ValidationError("No Transfer was found")

        print(transfer_ids)
        print("length of =", len(transfer_ids))

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        sheet.set_column(0, 5, 40)

        head = workbook.add_format({'bold': True, 'font_size': 30, 'align': 'center', 'underline': True})
        t_body = workbook.add_format({'align': 'center', 'border': 1})
        table_head = workbook.add_format({'bold': True, 'font_size': 15, 'align': 'center', 'border': 1})
        date_size = workbook.add_format({'font_size': 12, 'bold': True, 'align': 'center'})
        heading_key = ["Machine Name", "Transfer Type", "Customer Name", "Transfer Date"]
        len_transfer_ids = len(transfer_ids)
        cus_name = []
        for transfer in transfer_ids:
            if transfer["name"] not in cus_name:
                cus_name.append(transfer["name"])

        if len(cus_name) == 1:
            sheet.merge_range('A1:B4', 'MACHINE TRANSFER REPORT', head)
            if data['from_date'] and data['to_date']:
                sheet.set_row(11, 40)
                sheet.merge_range('A6:A7', 'From Date = ' + data['from_date'], date_size)
                sheet.merge_range('A8:A9', 'To Date = ' + data['to_date'], date_size)
                sheet.merge_range('C7:C8', 'Customer Name = ' + cus_name[0], date_size)
                row = 11
                col = 0
                for key in heading_key:
                    if key == "Customer Name":
                        continue
                    else:
                        sheet.write(row, col, key, table_head)
                        col += 1
                t_row = 12
                col = 0
                for doc in transfer_ids:
                    values = []
                    for key in doc:
                        if key == 'transfer_date':
                            t_date = doc[key].strftime('%d-%m-%Y')
                            values.append(t_date)
                        elif key == 'machine_name' or key == 'transfer_type':
                            field_value = doc[key].capitalize()
                            values.append(field_value)
                        elif key == 'name':
                            continue
                        else:
                            values.append(doc[key])
                    sheet.write_row(t_row, col, tuple(values), t_body)
                    t_row += 1
            else:
                sheet.merge_range('A6:A7', 'Customer Name = ' + cus_name[0], date_size)
                sheet.set_row(9, 40)
                row = 9
                col = 0
                for key in heading_key:
                    if key == "Customer Name":
                        continue
                    else:
                        sheet.write(row, col, key, table_head)
                        col += 1

                t_row = 10
                col = 0
                for doc in transfer_ids:
                    values = []
                    for key in doc:
                        if key == 'transfer_date':
                            t_date = doc[key].strftime('%d-%m-%Y')
                            values.append(t_date)
                        elif key == 'machine_name' or key == 'transfer_type':
                            field_value = doc[key].capitalize()
                            values.append(field_value)
                        elif key == 'name':
                            continue
                        else:
                            values.append(doc[key])
                    sheet.write_row(t_row, col, tuple(values), t_body)
                    t_row += 1
        else:
            sheet.merge_range('B1:C4', 'MACHINE TRANSFER REPORT', head)
            if data['from_date'] and data['to_date']:
                sheet.set_row(11, 40)
                sheet.merge_range('A6:A7', 'From Date = ' + data['from_date'], date_size)
                sheet.merge_range('A8:A9', 'To Date = ' + data['to_date'], date_size)
                row = 11
                col = 0
                for key in heading_key:
                    sheet.write(row, col, key, table_head)
                    col += 1
                t_row = 12
                col = 0
                for doc in transfer_ids:
                    values = []
                    for key in doc:
                        if key == 'transfer_date':
                            t_date = doc[key].strftime('%d-%m-%Y')
                            values.append(t_date)
                        elif key == 'machine_name' or key == 'transfer_type':
                            field_value = doc[key].capitalize()
                            values.append(field_value)
                        else:
                            values.append(doc[key])
                    sheet.write_row(t_row, col, tuple(values), t_body)
                    t_row += 1
            else:
                sheet.set_row(6, 40)
                row = 6
                col = 0
                for key in heading_key:
                    sheet.write(row, col, key, table_head)
                    col += 1
                t_row = 7
                col = 0
                for doc in transfer_ids:
                    values = []
                    for key in doc:
                        if key == 'transfer_date':
                            t_date = doc[key].strftime('%d-%m-%Y')
                            values.append(t_date)
                        elif key == 'machine_name' or key == 'transfer_type':
                            field_value = doc[key].capitalize()
                            values.append(field_value)
                        else:
                            values.append(doc[key])
                    sheet.write_row(t_row, col, tuple(values), t_body)
                    t_row += 1

        sheet.merge_range('A20:A21', f"Total Transfer Count = {len_transfer_ids}", date_size)
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()


