from odoo import fields, models
class PurchaseOrderChangesHistory(models.Model):
    _name='purchase.order.changes.history'

    revision_number=fields.Integer(string="Revision Number")
    modified_user=fields.Char(string="Modified User")
    modified_date=fields.Datetime(string="Modified Date")
    changes_history=fields.Text(string="Changes History")
    purchase_order_id=fields.Many2one('purchase.order')
