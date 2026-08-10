{
    'name': "clear_cart",
    'version': "19.0.1.2",
    'category': 'Technical',
    'summary': """ Clearing the cart listed products""",
    'description': """By clicking the clear cart button and deleting all listed products from the cart """,
    'depends': ['base','sale','product','website_sale', 'web'],
    'data': ["views/cart_view.xml"],
    'assets': {
        'web.assets_frontend': ["clear_cart/static/src/clear_cart.js"]
    },
    'author': "demo company",
    'website': "https://www.demo_company.com",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,

}
