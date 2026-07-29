from odoo import api,fields,models,_
from odoo.exceptions import UserError
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    delivery_rating_selection=fields.Selection([('star0',' '),('star1',' * '),('star2',' * * '),('star3',' * * * '),('star4',' * * * * '),('star5',' * * * * * ')],compute="_compute_delivery_rating_selection",store=True)
    rating_status=fields.Boolean(string="Rating Status",default=lambda self:self.env['ir.config_parameter'].get_param('purchase_order_delivery_rating.is_delivery_rating'))
    partner_rating=fields.Selection([('star0',' '),('star1',' * '),('star2',' * * '),('star3',' * * * '),('star4',' * * * * '),('star5',' * * * * * ')],string="Vendor Rating",related="partner_id.vendor_rating")

    @api.depends('effective_date')
    def _compute_delivery_rating_selection(self):
        """ Function for computing delivery rating selection based on differance between expected delivery date and received date.
        Calculating the average rating for vendor based on every purchase order ratings and writes into vendor field """
        if self.date_planned and self.effective_date:
            print(self.date_planned)
            print(self.effective_date)
            planned_date = self.date_planned.date()
            received_date = self.effective_date.date()
            print(planned_date, received_date)
            days_differance = planned_date - received_date
            print(days_differance.days)
            if days_differance.days <= 0:
                self.write({'delivery_rating_selection':'star5'})
            elif days_differance.days > 0 and days_differance.days <= 2:
                self.write({'delivery_rating_selection': 'star4'})
            elif days_differance.days >= 3 and days_differance.days <= 5:
                self.write({'delivery_rating_selection': 'star3'})
            elif days_differance.days >= 6 and days_differance.days <= 10:
                self.write({'delivery_rating_selection': 'star2'})
            else:
                self.write({'delivery_rating_selection': 'star1'})
        else:
            self.write({'delivery_rating_selection':'star0'})

        purchase_order_ids = self.partner_id.purchase_order_ids
        print(purchase_order_ids)
        star1 = 0
        star2 = 0
        star3 = 0
        star4 = 0
        star5 = 0

        for order in purchase_order_ids:
            print(order)
            print(order.delivery_rating_selection)
            if order.delivery_rating_selection:
                if order.delivery_rating_selection == 'star1':
                    star1 += 1
                elif order.delivery_rating_selection == 'star2':
                    star2 += 1
                elif order.delivery_rating_selection == 'star3':
                    star3 += 1
                elif order.delivery_rating_selection == 'star4':
                    star4 += 1
                else:
                    star5 += 1

            else:
                continue

        print(star1, star2, star3, star4, star5)
        total_po_star = len(purchase_order_ids) * 5
        print("total_po_star", total_po_star)
        vendor_received_star = (star1 * 1) + (star2 * 2) + (star3 * 3) + (star4 * 4) + (star5 * 5)
        print("vendor_received_star", vendor_received_star)
        if vendor_received_star == 0:
            self.partner_id.write({'vendor_rating':'star0'})
        else:
            avarage_stars = (vendor_received_star / total_po_star) * 100
            print("avarage_stars", avarage_stars)
            if avarage_stars < 20:
                self.partner_id.write({'vendor_rating': 'star1'})
            elif avarage_stars < 40:
                self.partner_id.write({'vendor_rating': 'star2'})
            elif avarage_stars < 60:
                self.partner_id.write({'vendor_rating': 'star3'})
            elif avarage_stars < 80:
                self.partner_id.write({'vendor_rating': 'star4'})
            else:
                self.partner_id.write({'vendor_rating': 'star5'})


    def button_confirm(self):
        res= super().button_confirm()
        print('partner_rating',self.partner_rating)
        if self.partner_rating and self.rating_status==True:
         if self.partner_rating=="star1" or self.partner_rating=="star2":
            raise UserError(_("Selectable Vendor Has Low Delivery Rating."))

        return res
