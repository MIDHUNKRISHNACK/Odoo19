{
    'name': "pos_rating",
    'version': "19.0.1.2",
    'category': 'Technical',
    'summary': """ Displays an rating on each products in pos product list view and pos receipt""",
    'description': """ Chooses an rating for particular product from back end and displays it on top left corner of pos product view """,
    'depends': ['base','sale','product',"point_of_sale",'web'],
    'data': [
        "views/product_template_view.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_rating/static/src/xml/new_alert_dialog.xml",
            "pos_rating/static/src/js/new_alert_dialog.js",
             "pos_rating/static/src/js/pos_product_card.js",
             "pos_rating/static/src/xml/pos_product_card_view.xml",

        ]},
    'author': "demo company",
    'website': "https://www.demo_company.com",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
}