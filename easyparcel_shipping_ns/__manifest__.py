# -*- coding: utf-8 -*-

{
    "name": "Easyparcel Shipping Integration",
    'version': '15.0',
    "category": "General",
    'summary': "This integration helps to connect Easyparcel to your Odoo E-commerce website. You can perform various operations like get live shipping rate, generate shipment labels, track shipment. Couriers include J&T, Pos Laju, Pgeon, Skynet and many more.",
    "description": "Easyparcel Shipping Connector",
    "author": "Wizeewig (Softlakes Sdn. Bhd)",
    "depends": ['website_sale', 'website_sale_delivery'],
    "data": [
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/sale_order.xml',
        'views/stock_picking.xml',
        'views/choose_delivery_carrier.xml',
        'views/delivery_carrier.xml',
        'views/shipping_backbone_ns.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'easyparcel_shipping_ns/static/src/css/easyparcel.css',
            'easyparcel_shipping_ns/static/src/js/easyparcel.js'
        ]
    },
    'auto_install': False,
    'installable': True,
    'application': True,
    'qweb': [],

    'images': ['static/description/EasyParcel-logo-dark.png' , 'static/description/icon.png'] ,

    "website": "https://www.wiz.asia",
    'support': 'help@wiz.asia',
    'maintainer': 'Wizeewig (Softlakes Sdn. Bhd)',
    'license': 'OPL-1',
    'price': '175',
    'currency': 'USD',
}
