import json
from odoo import http
from odoo.http import content_disposition, request, serialize_exception
from odoo.tools import html_escape

class XLSXReportController(http.Controller):

    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'],
                csrf=False)
    def get_report_xlsx(self, model, options, output_format, report_name):
        """Function for receiving field values from js file and calls inside the abstract model function"""
        print("model", model)
        print("options", options)
        print("output_format", output_format)
        print(" request.env[model]=", request.env[model])
        report_obj = request.env[model].with_user(request.session.uid)
        print(" report_obj=", report_obj)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(report_name + '.xlsx'))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))