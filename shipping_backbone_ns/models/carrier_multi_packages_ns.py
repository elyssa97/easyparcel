# -*- coding: utf-8 -*-

from odoo import api, fields, models


class CarrierMultiPackages(models.Model):
    _name = 'carrier.multi.packages.ns'
    _description = 'Multi Carrier Packages'

    parcel_number = fields.Char(string='Parcel Number', copy=False)
    parcel_id = fields.Char(string='Parcel ID', copy=False)
    parcel_status = fields.Char(string='Parcel Status', copy=False)
    parcel_state = fields.Selection([('active', 'Active'), ('cancel', 'Canceled')],
                                    string='Parcel State', default='active')
    tracking_url = fields.Char(string='Tracking URL', copy=False)
    picking_id = fields.Many2one('stock.picking', string='Shipstation Instance')
