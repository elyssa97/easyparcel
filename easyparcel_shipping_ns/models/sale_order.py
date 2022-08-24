# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EasyParcelSaleOrder(models.Model):
    _inherit = 'sale.order'

    easyparcel_service = fields.Char(copy=False, string='EasyParcel Service')

