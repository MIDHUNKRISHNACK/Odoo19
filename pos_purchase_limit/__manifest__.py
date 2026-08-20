{
    'name': "pos_purchase_limit",
    'version': "19.0.1.2",
    'category': 'Technical',
    'summary': """ Displaying an alert message if purchase limit is exceeded for an customer """,
    'description': """ user can set an purchase limit to the customer and if the customer purchases more than the limit shown an alert message """,
    'depends': ['base','sale','product',"point_of_sale",'web'],
    'data': [ "views/res_config_settings_view.xml",
              "views/res_partner_view.xml",
             ],
    "assets": {
        "point_of_sale._assets_pos": [
           "pos_purchase_limit/static/src/js/purchase_limit.js",

        ]},
    'author': "demo company",
    'website': "https://www.demo_company.com",
    'sequence': -10,
    'application': True,
    'installable': True,
    'auto_install': True,
}