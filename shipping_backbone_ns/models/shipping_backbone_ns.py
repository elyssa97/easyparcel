# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class ShippingBackBone(models.Model):
    _name = 'shipping.backbone.ns'
    _description = 'Shipping Backbone'
    _rec_name = 'name'

    name = fields.Char(string="Name")
    shipping_provider = fields.Selection([], string="Shipping Provider")
    use_warehouse_address = fields.Boolean(string='Use Warehouse Address As Sender Address', default=True)
    sender_address = fields.Many2one('res.partner', string='Sender Address')
    template_id = fields.Many2one('mail.template', string='Mail Template')
    auto_send_mail = fields.Boolean(string='Send Shipment Confirmation Mail')
    color = fields.Integer(string='Color Index', help="select color")

    # custom rate field
    # custom_rates_flag = fields.Boolean(string='Custom Rates')

    mail_template_id = fields.Many2one('mail.template', 'Mail Template')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Name is already exists !"),
    ]

    def button_delivery_method(self):
        """
        Redirect to delivery method
        """
        return {
            'name': _('Delivery Method'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'delivery.carrier',
            'view_id': False,
            'type': 'ir.actions.act_window',
        }

    def check_required_value(self, require_filed, sender, receiver):
        """
        Check the  all required parameter
        :return True
        """
        for address in [sender, receiver]:
            missing_field = [field for field in require_filed if not address[field]]
            if missing_field:
                raise ValidationError(_("Missing {0} in {1}").format(', '.join(missing_field), address.name))
        return True

    def order_line_product_weight(self, order):
        """
        total of all product weight
        """
        product = order.order_line.filtered(lambda order_line: order_line.is_delivery == False)
        return sum(product.mapped('product_id.weight'))

    def shipping_backbone_open_instance_view(self):
        form_id = self.env.ref('shipping_backbone_ns.shipping_backbone_ns_view_form')
        action = {
            'name': _('Process Configuration Instance'),
            'view_id': False,
            'res_model': 'shipping.backbone.ns',
            'context': self._context,
            'view_mode': 'form',
            'res_id': self.id,
            'views': [(form_id.id, 'form')],
            'type': 'ir.actions.act_window',
        }
        return action

    def delivery_order_instance_view(self):
        carrier_id = self.env['delivery.carrier'].search([('shipping_provider_ns', '=', self.id)])
        action = self.env.ref('stock.action_picking_tree_all').read()[0]
        action['domain'] = [('carrier_id', 'in', carrier_id.ids)]
        return action
