from odoo import fields, models, _
from odoo.addons.delivery.models.delivery_carrier import DeliveryCarrier


# def rate_shipment(self, order):
#     self.ensure_one()
#     if hasattr(self, '%s_rate_shipment' % self.delivery_type):
#         if self.custom_rates_flag:
#             if self.custom_rate_charge_type == 'fixed':
#                 res = self.fixed_rate_shipment(order)
#             if self.custom_rate_charge_type == 'base_on_rule':
#                 res = self.base_on_rule_rate_shipment(order)
#         else:
#             res = getattr(self, '%s_rate_shipment' % self.delivery_type)(order)
#         # apply margin on computed price
#         res['price'] = float(res['price']) * (1.0 + (self.margin / 100.0))
#         # save the real price in case a free_over rule overide it to 0
#         res['carrier_price'] = res['price']
#         # free when order is large enough
#         if res['success'] and self.free_over and order._compute_amount_total_without_delivery() >= self.amount:
#             res['warning_message'] = _('The shipping is free since the order amount exceeds %.2f.') % (self.amount)
#             res['price'] = 0.0
#         return res


# DeliveryCarrier.rate_shipment = rate_shipment


class DeliveryCarrier(models.Model):
    _inherit = 'delivery.carrier'

    shipping_provider_ns = fields.Many2one('shipping.backbone.ns', string='Shipping Provider')
    # custom_rates_flag = fields.Boolean(related='shipping_provider_ns.custom_rates_flag', store=True, copy=False)
    custom_rate_charge_type = fields.Selection([('fixed', 'Fixed Price'), ('base_on_rule', 'Based on Rules')],
                                               string='Pricing', default="fixed", copy=False)

