from odoo import api,fields,models,_
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    delivery_rating=fields.Char(string="Delivery Rating",readonly=True,compute="_compute_delivery_rating",store=True)
    rating_status=fields.Boolean(string="Rating Status",default=lambda self:self.env['ir.config_parameter'].get_param('purchase_order_delivery_rating.is_delivery_rating'))
    partner_rating=fields.Char(string="Vendor Rating",compute="_compute_partner_rating")


    @api.depends('partner_id')
    def _compute_partner_rating(self):
        print("a")
        partner_rating=self.partner_id.vendor_rating
        self.partner_rating=partner_rating


    @api.depends('effective_date')
    def _compute_delivery_rating(self):
        print("kkkkkkkkkkkkkk")
        if self.date_planned and self.effective_date:
            print(self.rating_status)
            print(self.date_planned)
            print(self.effective_date)
            planned_date=self.date_planned.date()
            received_date=self.effective_date.date()
            print(planned_date,received_date)
            days_differance=planned_date-received_date
            print(days_differance.days)
            if days_differance.days <= 0:
                self.delivery_rating=" * * * * * "
            elif days_differance.days >0 and days_differance.days <=2:
                self.delivery_rating=" * * * * "
            elif days_differance.days >=3 and days_differance.days <=5:
                self.delivery_rating=" * * * "
            elif days_differance.days >=6 and days_differance.days <=10:
                self.delivery_rating=" * * "
            else :
                self.delivery_rating=" * "
        else:
            self.delivery_rating=" "

        purchase_order_ids = self.partner_id.purchase_order_ids
        print(purchase_order_ids)
        star1 = 0
        star2 = 0
        star3 = 0
        star4 = 0
        star5 = 0

        for order in purchase_order_ids:
            print(order)
            print(order.delivery_rating)
            if order.delivery_rating:
                if order.delivery_rating == " * ":
                    star1 += 1
                elif order.delivery_rating == " * * ":
                    star2 += 1
                elif order.delivery_rating == " * * * ":
                    star3 += 1
                elif order.delivery_rating == " * * * * ":
                    star4 += 1
                else:
                    star5 += 1

            else:
                continue

        print(star1, star2, star3, star4, star5)
        total_po_star = len(purchase_order_ids) * 5
        print("total_po_star", total_po_star)
        if total_po_star:
            vendor_received_star = (star1 * 1) + (star2 * 2) + (star3 * 3) + (star4 * 4) + (star5 * 5)
            print("vendor_received_star", vendor_received_star)
            avarage_stars = (vendor_received_star / total_po_star) * 100
            print("avarage_stars", avarage_stars)
            if avarage_stars < 20:
                self.partner_id.vendor_rating = " * "
            elif avarage_stars < 40:
                self.partner_id.vendor_rating = " * * "
            elif avarage_stars < 60:
                self.partner_id.vendor_rating = " * * * "
            elif avarage_stars < 80:
                self.partner_id.vendor_rating = " * * * * "
            else:
                self.partner_id.vendor_rating = " * * * * * "



        # print(star1, star2, star3, star4, star5)
        # total_po_stars = len(purchase_order_ids) * 5
        # print("total_po_stars", total_po_stars)
        # rating_division = total_po_stars / 5
        # print("rating division", rating_division)
        # total_vendor_star = star1 + star2 + star3 + star4 + star5
        # print("total_vendor_star", total_vendor_star)
        #
        # if total_vendor_star < rating_division:
        #     self.partner_id.vendor_rating = " * "
        # elif total_vendor_star < (rating_division * 2):
        #     self.partner_id.vendor_rating = " * * "
        # elif total_vendor_star < (rating_division * 3):
        #     self.partner_id.vendor_rating = " * * * "
        # elif total_vendor_star < (rating_division * 4):
        #     self.partner_id.vendor_rating = " * * * * "
        # else:
        #     self.partner_id.vendor_rating = " * * * * * "

    def button_confirm(self):
        res= super().button_confirm()
        print('partner_rating',self.partner_rating)
        if self.partner_rating==" * " or self.partner_rating==" * * ":
            raise UserError(_("Selectable Vendor Has Low Delivery Rating."))

        # if star1 > star2 and star1 > star3 and star1 > star4 and star1 > star5:
        #     self.partner_id.vendor_rating = " * "
        # elif star2 > star3 and star2 > star4 and star2 > star5:
        #     self.partner_id.vendor_rating = " * * "
        # elif star3 > star4 and star3 > star5:
        #     self.partner_id.vendor_rating = " * * * "
        # elif star4 > star5:
        #     self.partner_id.vendor_rating = " * * * * "
        # else:
        #     self.partner_id.vendor_rating = " * * * * * "


        return res
