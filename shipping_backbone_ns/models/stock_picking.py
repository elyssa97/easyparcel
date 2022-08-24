from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_done(self):
        """
        send shipment confirmation mail to the customer
        """
        action_done = super(StockPicking, self).action_done()
        auto_send_mail = self.carrier_id and self.carrier_id.shipping_provider_ns and \
                         self.carrier_id.shipping_provider_ns.auto_send_mail
        if auto_send_mail:
            # send mail to the customer
            mail_template_id = self.carrier_id and self.carrier_id.shipping_provider_ns and \
                               self.carrier_d.shipping_provider_ns.mail_template_id
            if mail_template_id:
                mail_template_id.send_mail(self.id, True)
        return action_done
