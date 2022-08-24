# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EasyParcelShipping(models.Model):
    _inherit = 'shipping.backbone.ns'

    shipping_provider = fields.Selection(selection_add=[("easyparcel", "Easyparcel")])

    easyparcel_api_key = fields.Char(string='API KEY', copy=False)

