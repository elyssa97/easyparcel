# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from .easyparcel_request import EasyParcelRequest
from .easyparcel_request import filter_error_message
from odoo.addons.easyparcel_shipping_ns.models.easyparcel_response import EasyParceResponse


class ShippingDelivery(models.Model):
    _inherit = 'delivery.carrier'

    delivery_type = fields.Selection(selection_add=[("easyparcel_ns", "EasyParcel")],
                                     ondelete={'easyparcel_ns': 'set default'})
    easyparcel_package_ns_id = fields.Many2one('stock.package.type', string="EasyParcel Package")

    def easyparcel_ns_rate_shipment(self, order):
        warehouse_address_flag = self.shipping_provider_ns and self.shipping_provider_ns.use_warehouse_address
        if warehouse_address_flag:
            sender_add = order and order.warehouse_id and order.warehouse_id.partner_id
        else:
            sender_add = self.shipping_provider_ns and self.shipping_provider_ns.sender_address
        request_body = EasyParcelRequest.rate_body(self, sender_add=sender_add, receiver_add=order and order.partner_id,
                                                   order=order)
        status, code, response_data = EasyParcelRequest.send_request(self, service='live_rate', body=request_body)
        # status = True
        # response_data = EasyParceResponse.rate_response(self)
        if status:
            error_code = response_data.get('error_code')
            if error_code in [0, '0']:
                for rates in response_data.get('result'):
                    self.save_rate_response(response_data=rates)
                    service_id = self.env['easyparcel.shipping.carrier'].search([('sale_id', '=', order and order.id)],
                                                                                order="price desc", limit=1)
                    price = service_id and service_id.price or 0.0
                    return {'success': True, 'price': float(price) or 0.0, 'error_message': False, 'warning_message': False}
            else:
                error_msg = filter_error_message(service='rate_shipment', response=response_data)
                return {'success': False, 'price': 0.0, 'error_message': error_msg, 'warning_message': False}
        else:
            return {'success': False, 'price': 0.0, 'error_message': response_data, 'warning_message': False}

    def save_rate_response(self, response_data, order_id=False):
        """
        save rate api service response data into odoo
        :param response_data: response data
        """
        carrier_id = self.env['choose.delivery.carrier'].search(
            [('order_id', '=', self._context.get('active_id'))], order='id desc', limit=1)
        exist_record = self.env['easyparcel.shipping.carrier'].search(
            [('sale_id', 'in', [self._context.get('active_id') or order_id and order_id.id])])
        if exist_record:
            exist_record.unlink()
        if carrier_id and carrier_id.easyparcel_shipping_ids:
            carrier_id.easyparcel_shipping_ids = [(5, 0, 0)]
        for carrier in response_data.get('rates'):
            carrier_data = {
                'delivery': carrier.get('delivery'),
                'rate_id': carrier.get('rate_id'),
                'service_id': carrier.get('service_id'),
                'price': carrier.get('price'),
                'service_name': carrier.get('service_name'),
                'courier_name': carrier.get('courier_name'),
                'choose_carrier_id': carrier_id and carrier_id.id,
                'sale_id': order_id and order_id.id if order_id else self._context.get('active_id')
            }
            self.env['easyparcel.shipping.carrier'].create(carrier_data)

    @api.model
    def easyparcel_ns_send_shipping(self, pickings):
        request_body = EasyParcelRequest.shipment_body(self, pickings)
        status, code, response_data = EasyParcelRequest.send_request(self, service='create_shipment', body=request_body)
        if status:
            error_code = response_data.get('error_code')
            if error_code in [0, '0']:
                result = response_data.get('result')
                if isinstance(result, list):
                    result = result[0]
                else:
                    result = [result]
                parcel_number = result and result.get('parcel_number')
                order_number = result and result.get('order_number')
                if not parcel_number and not order_number:
                    error_msg = filter_error_message(service='rate_shipment', response=response_data)
                    raise ValidationError(_(error_msg))
                pickings.ep_parcel_number = parcel_number
                price = result and result.get('price') or 0.0
                shipping_data = {
                    'exact_price': float(price) or 0.0,
                    'tracking_number': order_number}
                shipping_data = [shipping_data]
                return shipping_data
            else:
                error_msg = filter_error_message(service='rate_shipment', response=response_data)
                raise ValidationError(_(error_msg))
        else:
            raise ValidationError(_(response_data))

    def easyparcel_ns_get_tracking_link(self, picking):
        return '{}'.format(picking.ep_tracking_url)

    def easyparcel_ns_cancel_shipment(self, pickings):
        raise ValidationError(_("CANCEL SERVICE NOT PROVIDE BY EASYPARCEL"))
