from odoo import http
from odoo.http import request

class MachineServiceTemplateController(http.Controller):
    @http.route('/clear_cart', type='http', auth='public', website=True)
    def clear_cart(self):
        """Function to clear cart items and updating the cart item count"""
        request.cart.order_line.unlink()
        if 'website_sale_cart_quantity' not in request.session:
            return request.cart.cart_quantity
        request.session['website_sale_cart_quantity']=0

        return request.redirect('/shop/cart')




