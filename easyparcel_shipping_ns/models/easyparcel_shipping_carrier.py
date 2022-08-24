# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class EasyParcelShippingCarrier(models.TransientModel):
    _name = 'easyparcel.shipping.carrier'
    _description = 'Easy parcel Shipping Carrier'

    delivery = fields.Char(string='Delivery', copy=False)
    rate_id = fields.Char(string='Rate ID', copy=False)
    service_id = fields.Char(string='Service ID', copy=False)
    price = fields.Float(string='Price', copy=False)
    service_name = fields.Char(string='Service Name')
    courier_name = fields.Char(string='Courier Name')
    sale_id = fields.Many2one('sale.order', string='Sale Order')

    choose_carrier_id = fields.Many2one('choose.delivery.carrier', string='Choose Carrier ID', copy=False)

    def set_carrier(self):
        self.choose_carrier_id.write(
            {'delivery_price': self.price, 'display_price': self.price})
        if self.sale_id:
            self.sale_id.easyparcel_service = self.service_id
            self.sale_id.amount_delivery = float(self.price) or 0
            delivery_line = self.sale_id.order_line.filtered(lambda order_line: order_line.is_delivery == True)
            if delivery_line:
                delivery_line[0].price_total = float(self.price) or 0
        return {
            'name': _('Add a shipping method'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'choose.delivery.carrier',
            'res_id': self.choose_carrier_id.id,
            'target': 'new',
        }
