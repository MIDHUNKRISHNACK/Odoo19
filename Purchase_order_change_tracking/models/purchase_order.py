import datetime
from odoo import api, fields, models
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _name = "purchase.order"

    history_ids=fields.One2many('purchase.order.changes.history',"purchase_order_id")


    def write(self, vals):
        print(self)
        print(self.history_ids)
        len_history_records=len(self.history_ids)
        print(len_history_records)
        if  self.state=='sent':
            print(vals)
            print(self)
            note=""
            change=vals.keys()
            for change in change:
                if change!="order_line":
                    if change=="partner_id":
                        print(change)
                        note+=str("Vendor Name is Changed to "+str(self.env['res.partner'].browse(vals[change]).name))
                    else:
                        note+=str(change+"  has changed to  "+str(vals[change]) +" , ")
                        print(note)
                    self.env['purchase.order.changes.history'].create({
                        'purchase_order_id':self.id,
                        'revision_number': len_history_records + 1,
                        'modified_user': self.env.user.partner_id.name,
                        'modified_date': datetime.datetime.now(),
                        'changes_history': note,
                    })
                    break
                else:
                   for rec in vals[change]:
                       if rec[0]==1:
                           print(len(rec[2]))
                           if len(rec[2])==2:
                               order_line_id=self.env['purchase.order.line'].browse(rec[1])
                               product_name=order_line_id.product_id.name
                               print(product_name)
                               note += str("product_qty of the product  "+product_name+"  has changed to  "+str(rec[2]['product_qty'])+" , "+"price_unit of the product  "+product_name+"  has changed to  "+str(rec[2]['price_unit'])+" , ")
                               print(note)
                               self.env['purchase.order.changes.history'].create({
                                   'purchase_order_id': self.id,
                                   'revision_number':len_history_records + 1 ,
                                   'modified_user': self.env.user.partner_id.name,
                                   'modified_date': datetime.datetime.now(),
                                   'changes_history': note,
                               })
                           elif rec[2].get('product_qty', False):
                               order_line_id = self.env['purchase.order.line'].browse(rec[1])
                               product_name = order_line_id.product_id.name
                               note += str("product_qty of the product  " + product_name + "  has changed to  " + str(rec[2]['product_qty']) + " , ")
                               print(note)
                               self.env['purchase.order.changes.history'].create({
                                   'purchase_order_id': self.id,
                                   'revision_number': len_history_records + 1,
                                   'modified_user': self.env.user.partner_id.name,
                                   'modified_date': datetime.datetime.now(),
                                   'changes_history': note,
                               })
                           else :
                               order_line_id = self.env['purchase.order.line'].browse(rec[1])
                               product_name = order_line_id.product_id.name
                               note += str("price_unit of the product  "+product_name+"  has changed to  "+str(rec[2]['price_unit'])+" , ")
                               print(note)
                               self.env['purchase.order.changes.history'].create({
                                   'purchase_order_id': self.id,
                                   'revision_number': len_history_records + 1,
                                   'modified_user': self.env.user.partner_id.name,
                                   'modified_date': datetime.datetime.now(),
                                   'changes_history': note,

                               })
                       elif rec[0]==2:
                           print(vals)
                           deleted_order_line=self.env['purchase.order.line'].browse(rec[1])
                           print(deleted_order_line)
                           print(deleted_order_line.product_id.name)
                           note=" The product "+str(deleted_order_line.product_id.name)+" has been deleted from order line"
                           print(note)
                           self.env['purchase.order.changes.history'].create({
                               'purchase_order_id': self.id,
                               'revision_number': len_history_records + 1,
                               'modified_user': self.env.user.partner_id.name,
                               'modified_date': datetime.datetime.now(),
                               'changes_history': note,

                           })
                       else:
                           new_product_id = self.env['product.product'].browse(rec[2].get('product_id'))
                           print(new_product_id)
                           print(new_product_id.name)
                           note += str(" New product "+ new_product_id.name+" is  Added to the Order Line " + " With the Quantity " + str(
                               rec[2]['product_qty']) + " and With Amount  "+str(rec[2]['price_unit']))
                           print(note)
                           self.env['purchase.order.changes.history'].create({
                               'purchase_order_id': self.id,
                               'revision_number': len_history_records + 1,
                               'modified_user': self.env.user.partner_id.name,
                               'modified_date': datetime.datetime.now(),
                               'changes_history': note,

                           })


        return super().write(vals)



    def action_open_history(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'purchase_order_history',
            'res_model': 'purchase.order.changes.history',
            'domain': [('purchase_order_id', '=', self.id)],
            'view_mode': 'list',
            }




