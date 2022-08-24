import logging
from odoo.http import request
from odoo import fields, http, tools, _
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.easyparcel_shipping_ns.models.easyparcel_request import EasyParcelRequest
from odoo.addons.easyparcel_shipping_ns.models.easyparcel_response import EasyParceResponse
_logger = logging.getLogger('EasyParce NS::')


class WebsiteSaleDelivery(WebsiteSale):
    @http.route()
    def update_eshop_carrier(self, **post):
        result = super(WebsiteSaleDelivery, self).update_eshop_carrier(**post)
        order = request.website.sale_get_order()
        if order:
            order.carrier_id = result.get('carrier_id')
        return result


class WebsiteSale(http.Controller):

    @http.route(['/easyparcel_service'], type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def easyparcel_service(self, **post):
        results = {}
        if post.get('order') and post.get('delivery_type'):
            delivery_method = request.env['delivery.carrier'].sudo().browse(int(post.get('delivery_type')))
            order = request.website.sale_get_order()
            if delivery_method.delivery_type == 'easyparcel_ns':
                results = request.env['ir.ui.view']._render_template(
                    'easyparcel_shipping_ns.easyparcel_carrier_service')
            if order and order.carrier_id:
                existing_records = request.env['easyparcel.shipping.carrier'].sudo().search(
                    [('sale_id', '=', order.id)])
                existing_records.sudo().unlink()
        return results

    @http.route(['/easyparcel_get_carriers'], type='json', auth='public', methods=['POST'],
                website=True, csrf=False)
    def easyparcel_get_carriers(self, **post):
        order = request.website.sale_get_order()
        try:
            carrier_id = order and order.carrier_id
            warehouse_address_flag = carrier_id.shipping_provider_ns and carrier_id.shipping_provider_ns.use_warehouse_address
            if warehouse_address_flag:
                sender_add = order and order.warehouse_id and order.warehouse_id.partner_id
            else:
                sender_add = carrier_id.shipping_provider_ns and carrier_id.shipping_provider_ns.sender_address
            request_body = EasyParcelRequest.rate_body(carrier_id, sender_add=sender_add,
                                                       receiver_add=order and order.partner_id,
                                                       order=order)
            status, code, response_data = EasyParcelRequest.send_request(carrier_id, service='live_rate',
                                                                         body=request_body)
            # status = True
            # response_data = EasyParceResponse.rate_response(self)
            if status:
                for rates in response_data.get('result'):
                    carrier_id.save_rate_response(response_data=rates, order_id=order)
            values = {
                'locations': request.env['easyparcel.shipping.carrier'].search(
                    [('sale_id', '=', order and order.id)]) or []
            }
            template = request.env['ir.ui.view']._render_template('easyparcel_shipping_ns'
                                                                  '.easyparcel_carrier_details', values)

            return {'template': template}
        except Exception as e:
            return {
                'error': "Location not found. Please enter proper shipping details or contact us for support.\n\n{}".format(
                    e)}

    @http.route(['/set_easyparcel_carrier_service'], type='json', auth='public', website=True, csrf=False)
    def set_easyparcel_carrier_service(self, location=False, **post):
        location_id = request.env['easyparcel.shipping.carrier'].browse(location)
        sale_id =  location_id and location_id.sale_id
        if location_id and location_id.id:
            # location_id.set_carrier()
            sale_id.amount_delivery = float(location_id.price) or 0
            location_id.sale_id.easyparcel_service = location_id.service_id
            delivery_line = sale_id.order_line.filtered(lambda order_line: order_line.is_delivery == True)
            if delivery_line:
                delivery_line[0].price_unit = float(location_id.price) or 0
            return {'success': True, 'courier_name': location_id.courier_name, 'service_name': location_id.service_name,
                    'price': location_id.price, 'amount_untaxed':sale_id.amount_untaxed, 'amount_total':sale_id.amount_total}
