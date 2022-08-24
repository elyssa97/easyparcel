# -*- coding: utf-8 -*-

{
    "name": "Shipping Connector",
    "version": "15.17.8.2022",
    "category": "General",
    'summary': "Connect your Odoo erp with bunch of shipping provider like dhl, usps, dsv,fedex, tnt, ups, shipstation, gls, correos, easyship, amazone, shopify, woocommerce, ebay, etc",
    "description": """
        Backbone for Shipping Integration
    """,
    "author": "NsInfosystem",
    "depends": ['delivery'],
    "data": [
        'security/ir.model.access.csv',
        'views/delivery_carrier.xml',
        'views/shipping_backbone_ns.xml',
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
    'qweb': [],

    'images': ['static/description/cover.jpeg'],

    "website": "https://nsinfosystem.com/",
    'support': 'contact@nsinfosystem.com/',
    'maintainer': 'NsInfosystem',

    "price": "9.99",
    "currency": "EUR",
    'license': 'OPL-1',
}
# 15.1
# carrier multi package


# 15.17.8.2022
# remove custom rate bug
