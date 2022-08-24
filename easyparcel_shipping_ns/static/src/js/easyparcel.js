odoo.define('easyparcel_shipping_ns.checkout', function (require) {
    'use strict';

    var core = require('web.core');
    var publicWidget = require('web.public.widget');

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var _t = core._t;
    var concurrency = require('web.concurrency');
    var dp = new concurrency.DropPrevious();
    var _onCarrierUpdateAnswer = function(result) {
		console.log('REsult -------------', result)
        var $amount_delivery = $('#order_delivery span.oe_currency_value');
        var $amount_untaxed = $('#order_total_untaxed span.oe_currency_value');
        var $amount_tax = $('#order_total_taxes span.oe_currency_value');
        var $amount_total = $('#order_total span.oe_currency_value');
        var $carrier_badge = $('#delivery_carrier input[name="delivery_type"][value=' + result.carrier_id + '] ~ .badge:not(.o_delivery_compute)');
        var $compute_badge = $('#delivery_carrier input[name="delivery_type"][value=' + result.carrier_id + '] ~ .o_delivery_compute');
        var $discount = $('#order_discounted');

        if ($discount && result.new_amount_order_discounted) {
            // Cross module without bridge
            // Update discount of the order
            $discount.find('.oe_currency_value').text(result.new_amount_order_discounted);

            // We are in freeshipping, so every carrier is Free
            $('#delivery_carrier .badge').text(_t('Free'));


        }

        if (result.status === true) {
            $amount_delivery.text(result.new_amount_delivery);
            $amount_untaxed.text(result.new_amount_untaxed);
            $amount_tax.text(result.new_amount_tax);
            $amount_total.text(result.new_amount_total);
            $carrier_badge.children('span').text(result.new_amount_delivery);
            $carrier_badge.removeClass('d-none');
            $compute_badge.addClass('d-none');
            $pay_button.data('disabled_reasons').carrier_selection = false;
            $pay_button.prop('disabled', _.contains($pay_button.data('disabled_reasons'), true));


        }
        else {
            console.error(result.error_message);
            $compute_badge.text(result.error_message);
            $amount_delivery.text(result.new_amount_delivery);
            $amount_untaxed.text(result.new_amount_untaxed);
            $amount_tax.text(result.new_amount_tax);
            $amount_total.text(result.new_amount_total);
        }
    };
    publicWidget.registry.websiteSaleDelivery = publicWidget.Widget.extend({
        selector: '.oe_website_sale',
        events: {
            'change select[name="shipping_id"]': '_onSetAddress',
            'click #delivery_carrier input[name="delivery_type"]': '_onCarrierClick',
        },

        /**
         * @override
         */
        start: function () {
            var self = this;
            var $carriers = $('#delivery_carrier input[name="delivery_type"]');
            // Workaround to:
            // - update the amount/error on the label at first rendering
            // - prevent clicking on 'Pay Now' if the shipper rating fails
            if ($carriers.length > 0) {
                $carriers.filter(':checked').click();
            }
            var order_id = $('#sale_order_js').val();
            var delivery_id = $("#delivery_carrier input[name='delivery_type']").filter(':checked').val();
            if(order_id && delivery_id)
            {
                $('#service_table_js').remove();
                self._rpc({
                    route: '/easyparcel_service',
                    params: {
                        'order': order_id,
                        'delivery_type':delivery_id
                    },
                });
            }

            // Asynchronously retrieve every carrier price
            _.each($carriers, function (carrierInput, k) {
                self._showLoading($(carrierInput));
                self._rpc({
                    route: '/shop/carrier_rate_shipment',
                    params: {
                        'carrier_id': carrierInput.value,
                    },
                }).then(self._handleCarrierUpdateResultBadge.bind(self));
            });

            return this._super.apply(this, arguments);
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {jQuery} $carrierInput
         */
        _showLoading: function ($carrierInput) {
            $carrierInput.siblings('.o_wsale_delivery_badge_price').html('<span class="fa fa-spinner fa-spin"/>');
        },
        /**
         * @private
         * @param {Object} result
         */
        _handleCarrierUpdateResult: function (result) {
            this._handleCarrierUpdateResultBadge(result);
            var $payButton = $('#o_payment_form_pay');
            var $amountDelivery = $('#order_delivery .monetary_field');
            var $amountUntaxed = $('#order_total_untaxed .monetary_field');
            var $amountTax = $('#order_total_taxes .monetary_field');
            var $amountTotal = $('#order_total .monetary_field');

            if (result.status === true) {
                $amountDelivery.html(result.new_amount_delivery);
                $amountUntaxed.html(result.new_amount_untaxed);
                $amountTax.html(result.new_amount_tax);
                $amountTotal.html(result.new_amount_total);
//                $payButton.data('disabled_reasons').carrier_selection = false;
                var disabledReasons = $payButton.data('disabled_reasons') || {};
                disabledReasons.carrier_selection = false;


                $payButton.prop('disabled', _.contains($payButton.data('disabled_reasons'), true));
            } else {
                $amountDelivery.html(result.new_amount_delivery);
                $amountUntaxed.html(result.new_amount_untaxed);
                $amountTax.html(result.new_amount_tax);
                $amountTotal.html(result.new_amount_total);
            }
        },
        /**
         * @private
         * @param {Object} result
         */
        _handleCarrierUpdateResultBadge: function (result) {
            var $carrierBadge = $('#delivery_carrier input[name="delivery_type"][value=' + result.carrier_id + '] ~ .o_wsale_delivery_badge_price');

            if (result.status === true) {
                 // if free delivery (`free_over` field), show 'Free', not '$0'
                 if (result.is_free_delivery) {
                     $carrierBadge.text(_t('Free'));
                 } else {
                     $carrierBadge.html(result.new_amount_delivery);
                 }
                 $carrierBadge.removeClass('o_wsale_delivery_carrier_error');
            } else {
                $carrierBadge.addClass('o_wsale_delivery_carrier_error');
                $carrierBadge.text(result.error_message);
            }
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * @private
         * @param {Event} ev
         */
        _onCarrierClick: function (ev) {
            var self = this;
            $("button[name='get_location']").parent().parent().remove();
            //var $radio = $(ev.currentTarget).find('input[type="radio"]');
	    var $radio = $(ev.currentTarget);
            this._showLoading($radio);
            $radio.prop("checked", true);
            var $payButton = $('#o_payment_form_pay');
            $payButton.prop('disabled', true);
//            $payButton.data('disabled_reasons', $payButton.data('disabled_reasons') || {});
//            $payButton.data('disabled_reasons').carrier_selection = true;
            var disabledReasons = $payButton.data('disabled_reasons') || {};
            disabledReasons.carrier_selection = true;
            dp.add(this._rpc({
                route: '/shop/update_carrier',
                params: {
                    carrier_id: $radio.val(),
                },
            })).then(function(result){
                self._handleCarrierUpdateResult(result)
                /* Find Location */
                _onCarrierUpdateAnswer;
			    var vals = _onCarrierUpdateAnswer;
                $payButton.prop('disabled', true);
                /* ------- Star Ship service Charge define --------- */
                setTimeout(function()
                {
                    var order_id = $('#sale_order_mondial_js').val();
                    var delivery_id = $("#delivery_carrier input[name='delivery_type']").filter(':checked').val();
                    if(order_id && delivery_id)
                    {
                        $('#service_table_js').remove();
                        var values = {
                            'order': order_id,
                            'delivery_type':delivery_id
                        };
                        ajax.jsonRpc('/easyparcel_service', 'call', values).then(function (service) {
                            // if (service && !$('div').hasClass('mondial_relay_loc_js'))
                            if (service)
                            {
                                $('.mondial_relay_loc_js').remove();
                                $('.modal-backdrop').addClass('hidden');
                                $('#delivery_method').find('#delivery_'+ delivery_id +'').parents('.list-group-item').append(service);

                                /*
                                 Get location
                                */
                                var $get_location = $('button[name="easyparcel_get_carriers"]');
                                $get_location.on('click', function () {
                                    ajax.jsonRpc('/easyparcel_get_carriers', 'call').then(function (data) {
                                        if (!data.error && data.template)
                                        {
                                            $('#mondial_relayId').find('.modal-body').html('');
                                            $('#mondial_relayId').find('.modal-body').html(data.template);
                                        }
                                        else{
                                            $('#mondial_relayId').find('.modal-body').html('');
                                            $('#mondial_relayId').find('.modal-body').html(data.error);
                                        }

                                        /*
                                         Set location
                                        */
                                        $('button[name="set_easyparcel_carrier_service"]').click(function(){
                                            var loc_id = $(this).next('input[name="location"]').val();
                                            if(loc_id){
                                                ajax.jsonRpc('/set_easyparcel_carrier_service', 'call', {'location': parseInt(loc_id)}).then(function(data) {
                                                    if(data.success == true)
                                                    {
                                                        $('#mondial_relayId').find('button[name="close"]').trigger( "click" );
                                                        $('.disp_location').text('');
                                                        var easyparcel_service = data.courier_name +'('+data.service_name+ ')'+'.'
                                                        $('.disp_location').text(easyparcel_service);
                                                        $('#order_delivery span.oe_currency_value').text(data.price)
                                                        $("#delivery_carrier input[name='delivery_type']").filter(':checked').parent().find('span span').text(data.price)
											            $('#order_total_untaxed span.oe_currency_value').text(data.amount_untaxed);
											            $('#order_total span.oe_currency_value').text(data.amount_total);
                                                    }
                                                });
                                            }
                                        })
                                    })

                                });
                            }
                            else{
                                $('.mondial_relay_loc_js').remove();
                            }
                        });
                    }
                    else{
                        var msg = '<p class="text-danger mt4">Something wrong!!!</p>'
                        $('#delivery_method').find('#delivery_'+ delivery_id +'').parents('.list-group-item').append(msg);
                    }
                }, 1000);
                $payButton.prop('disabled', false);
            });
        },
        /**
         * @private
         * @param {Event} ev
         */
        _onSetAddress: function (ev) {
            var value = $(ev.currentTarget).val();
            var $providerFree = $('select[name="country_id"]:not(.o_provider_restricted), select[name="state_id"]:not(.o_provider_restricted)');
            var $providerRestricted = $('select[name="country_id"].o_provider_restricted, select[name="state_id"].o_provider_restricted');
            if (value === 0) {
                // Ship to the same address : only show shipping countries available for billing
                $providerFree.hide().attr('disabled', true);
                $providerRestricted.show().attr('disabled', false).change();
            } else {
                // Create a new address : show all countries available for billing
                $providerFree.show().attr('disabled', false).change();
                $providerRestricted.hide().attr('disabled', true);
            }
        },
    });
});