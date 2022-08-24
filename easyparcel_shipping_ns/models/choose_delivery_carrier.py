# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EasyParcelChooseDelivery(models.TransientModel):
    _inherit = 'choose.delivery.carrier'

    easyparcel_shipping_ids = fields.One2many('easyparcel.shipping.carrier', 'choose_carrier_id', copy=False,
                                              string='Easyparcel Shipping')

