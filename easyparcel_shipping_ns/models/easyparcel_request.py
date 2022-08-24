# -*- coding: utf-8 -*-
import json
import logging
import requests
from datetime import datetime

_logger = logging.getLogger("EasyParce")


def host_name(env):
    """
    :param env: Delivery carrier environment
    :return: hostname of Easyparcel API service
    """
    if env:
        return 'https://connect.easyparcel.my'
    else:
        return 'https://demo.connect.easyparcel.my'


def filter_error_message(service, response):
    """
    filter the error message from the api response
    :param service: api service
    :param response: api response
    :return: clear error message
    """
    # in rate api service error message comes in error_remark
    error_msg = response and response.get('error_remark', False)
    error_code = response and response.get('error_code', False)
    msg = '%s \n %s' % (error_code, error_msg if error_msg and error_code else response)
    result = response.get('result') and response.get('result')[0]
    if result:
        if result.get('status') == 'fail':
            return result.get('remarks') if result.get('remarks') else response
    return msg


class EasyParcelRequest():
    def send_request(self, service, body, label_url=False):
        """
        Send API requests to Easyparcel API service
        :param label_url: label url
        :param service: API service
        :param body: request body of API service
        :return: api response
        """
        hostname = host_name(env=self.prod_environment)
        headers = {
            'Content-Type': 'application/json'
        }
        if service == 'live_rate':
            url = hostname + '/?ac=EPRateCheckingBulk'
        elif service == 'create_shipment':
            url = hostname + '/?ac=EPSubmitOrderBulk'
        elif service == 'make_payment':
            url = hostname + '/?ac=EPPayOrderBulk'
        elif label_url:
            url = label_url
        try:
            _logger.info(":::: Send POST Request TO {}".format(url))
            _logger.info("::: Request Body {}".format(body))
            response = requests.request(method='POST', url=url, data=json.dumps(body), headers=headers)
        except Exception as error:
            _logger.error("{}".format(error))
            return False, False, error
        if response.status_code in [200, 201]:
            _logger.info("::::: Successfully Response From {}".format(url))
            _logger.info("::::: Status Code {}".format(response.status_code))
            _logger.info("::::: Response Data {}".format(response.text))
            data = response.text if label_url else response.json()
            return True, response.status_code, data
        else:
            _logger.info("::::: Response From {}".format(url))
            _logger.info("::::: Status Code {}".format(response.status_code))
            _logger.info("::::: Response Data {}".format(response.text))
            return False, response.status_code, response

    def rate_body(self, sender_add, receiver_add, order):
        """
        prepare rate API checking body
        :param sender_add: sender address (res.partner object)
        :param receiver_add: receiver address (res.partner object)
        :return: API request body for RateAPI service
        """
        required_field = ['zip', 'country_id', 'state_id']
        self.shipping_provider_ns.check_required_value(required_field, sender=sender_add,
                                                       receiver=receiver_add)
        weight = self.shipping_provider_ns.order_line_product_weight(order=order)
        key = self.shipping_provider_ns and self.shipping_provider_ns.easyparcel_api_key
        return {
            "authentication": "%s" % key,
            "api": "%s" % key,
            "bulk": [
                {
                    "pick_code": "%s" % sender_add.zip,
                    "pick_state": "%s" % sender_add.state_id and sender_add.state_id.code,
                    "pick_country": "%s" % sender_add.country_id and sender_add.country_id and sender_add.country_id.code,
                    "send_code": "%s" % receiver_add.zip,
                    "send_state": "%s" % receiver_add.state_id and receiver_add.state_id.code,
                    "send_country": "%s" % receiver_add.country_id and receiver_add.country_id.code,
                    "weight": "%s" % weight,
                    "width": "%s" % self.easyparcel_package_ns_id.width,
                    "length": "%s" % self.easyparcel_package_ns_id.packaging_length,
                    "height": "%s" % self.easyparcel_package_ns_id.height
                }
            ]
        }

    def shipment_body(self, pickings):
        """
        prepare request body for create shipment API service
        :param pickings: stock picking object
        :return: dict for create shipment API service
        """
        warehouse_address_flag = self.shipping_provider_ns and self.shipping_provider_ns.use_warehouse_address
        if warehouse_address_flag:
            shipper_address = pickings and pickings.sale_id and pickings.sale_id.warehouse_id and pickings.sale_id.warehouse_id.partner_id
        else:
            shipper_address = self.shipping_provider_ns and self.shipping_provider_ns.sender_address
        receiver_address = pickings and pickings.partner_id
        key = self.shipping_provider_ns and self.shipping_provider_ns.easyparcel_api_key
        body = {
            "api": key,
            "bulk": [
                {
                    "weight": "{}".format(pickings.shipping_weight),
                    "width": "{}".format(self.easyparcel_package_ns_id and self.easyparcel_package_ns_id.height),
                    "length": "{}".format(
                        self.easyparcel_package_ns_id and self.easyparcel_package_ns_id.packaging_length),
                    "height": "{}".format(self.easyparcel_package_ns_id and self.easyparcel_package_ns_id.width),
                    "content": "{}".format(pickings and pickings.name),
                    "value": "%s" % (pickings.sale_id.amount_total or 0.0),
                    "service_id": "%s" % pickings.sale_id.easyparcel_service,
                    "pick_point": "",
                    "pick_name": "{}".format(shipper_address and shipper_address.name),
                    "pick_company": "",
                    "pick_contact": "{}".format(shipper_address and shipper_address.phone or shipper_address.mobile),
                    "pick_mobile": "",
                    "pick_addr1": "{}".format(shipper_address and shipper_address.street),
                    "pick_addr2": "{}".format(shipper_address and shipper_address.street2),
                    "pick_addr3": "",
                    "pick_addr4": "",
                    "pick_city": "{}".format(shipper_address and shipper_address.city),
                    "pick_state": "{}".format(
                        shipper_address and shipper_address.state_id and shipper_address.state_id.code),
                    "pick_code": "{}".format(shipper_address and shipper_address.zip),
                    "pick_country": "{}".format(
                        shipper_address and shipper_address.country_id and shipper_address.country_id.code),
                    "send_point": "",
                    "send_name": "{}".format(receiver_address and receiver_address.name),
                    "send_company": "",
                    "send_contact": "{}".format(receiver_address and receiver_address.phone or receiver_address.mobile),
                    "send_mobile": "",
                    "send_addr1": "{}".format(receiver_address and receiver_address.street),
                    "send_addr2": "{}".format(receiver_address and receiver_address.street2),
                    "send_addr3": "",
                    "send_addr4": "",
                    "send_city": "{}".format(receiver_address and receiver_address.city),
                    "send_state": "{}".format(
                        receiver_address and receiver_address.state_id and receiver_address.state_id.code),
                    "send_code": "{}".format(receiver_address and receiver_address.zip),
                    "send_country": "{}".format(
                        receiver_address and receiver_address.country_id and receiver_address.country_id.code),
                    "collect_date": "{}".format(
                        datetime.now().strftime("%Y-%m-{}".format(int(datetime.now().strftime("%d")) + 1))),
                    "sms": "1",
                    "send_email": "{}".format(receiver_address and receiver_address.email),
                    "hs_code": ""
                }
            ]
        }
        return body

    def make_payment_body(self, carrier):
        """
        prepare request body for API
        :return: dict
        """
        key = carrier and carrier.shipping_provider_ns.easyparcel_api_key
        data = {
            "api": key,
            "bulk": [
                {
                    "order_no": "%s" % self.carrier_tracking_ref
                }
            ]
        }
        return data
