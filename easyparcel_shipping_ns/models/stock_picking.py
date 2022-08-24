# -*- coding: utf-8 -*-
import logging
import binascii
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from .easyparcel_request import EasyParcelRequest
from .easyparcel_request import filter_error_message
_logger = logging.getLogger("EasyParcel NS")

class EasyParcelStock(models.Model):
    _inherit = 'stock.picking'

    ep_parcel_number = fields.Char(string='EasyParcel Parcel Number', copy=False)
    ep_tracking_url = fields.Char(string='Tracking URL', copy=False)
    ep_awb_number = fields.Char(string='EasyParcel AWB Number', copy=False)
    ep_label_url = fields.Char(string='EasyParcel Label', copy=False)

    def make_order_payment_ep(self):
        """
        make order payment of Easyparcel shipment
        in response attach label in Odoo
        """
        request_body = EasyParcelRequest.make_payment_body(self, self.carrier_id)
        status, code, response_data = EasyParcelRequest.send_request(self.carrier_id, service='make_payment',
                                                                     body=request_body)
        if status:
            error_code = response_data.get('error_code')
            if error_code in [0, '0']:
                result = response_data.get('result')
                if isinstance(result, list):
                    result = result[0]
                else:
                    result = [result]
                parcel = result and result.get('parcel') and result.get('parcel')[0]
                awb = parcel and parcel.get('awb')
                label_url = parcel and parcel.get('awb_id_link')
                tracking_url = parcel and parcel.get('tracking_url')
                if not awb and not tracking_url:
                    raise ValidationError(_(response_data))
                self.ep_tracking_url = tracking_url
                self.ep_awb_number = awb
                self.ep_label_url = label_url
                # self.attach_label_data(label_url=label_url)
            else:
                error_msg = filter_error_message(service='rate_shipment', response=response_data)
                raise ValidationError(error_msg)
        else:
            raise ValidationError(response_data)

    def attach_label_data(self, label_url):
        """
        attach label data into Odoo
        :param label_url: shipment label url
        """
        status, code, response_data = EasyParcelRequest.send_request(self.carrier_id, service=False,
                                                                     body=False, label_url=label_url)
        if status:
            self.message_post(body="EasyParcel AWB Label", attachments=[
                ('%s.%s' % ("{}".format(self.ep_awb_number), "pdf"), response_data)])
        else:
            _logger.info("::: SOMETHING WRONG TO ATTACH  LABEL {}".format(response_data))
