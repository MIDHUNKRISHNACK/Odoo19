from odoo import fields, models,api
class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_vendor_products=fields.Boolean(string="Vendor Products",default=False)
    vendor_product_ids=fields.Many2many('product.product',string="Vendor Products",compute="_compute_vendor_product_ids",store=True)
    demo=fields.Many2one('product.product',string="Demo Products",store=True)


    @api.depends("partner_id","is_vendor_products")
    def _compute_vendor_product_ids(self):

        for rec in self:
            if rec.is_vendor_products:
                print(rec.partner_id)
                vendor_product = self.env['product.product'].search([])
                filtered_vendor_product=vendor_product.filtered(lambda record:record.seller_ids.partner_id==rec.partner_id)
                print(vendor_product)
                print(filtered_vendor_product)

                rec.vendor_product_ids =[(fields.Command.set(filtered_vendor_product.ids))]
            else:
                vendor_product = self.env['product.product'].search([])
                rec.vendor_product_ids =[(fields.Command.set(vendor_product.ids))]


