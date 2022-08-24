from odoo import api, fields, models


class EasyParceResponse():
    def rate_response(self):
        return {
            "api_status": "Success",
            "error_code": "0",
            "error_remark": "",
            "result": [
                {
                    "REQ_ID": "",
                    "status": "Success",
                    "remarks": "",
                    "rates": [
                        {
                            "rate_id": "EP-RR0M2NL",
                            "service_detail": "dropoff/pickup",
                            "service_id": "EP-CS0CH",
                            "service_type": "parcel",
                            "courier_id": "EP-CR0A",
                            "courier_logo": "https://s3-ap-southeast-1.amazonaws.com/easyparcel-static/Public/source/general/img/couriers/Pos_Laju.jpg",
                            "scheduled_start_date": "2020-07-21 Tuesday",
                            "pickup_date": "2020-07-21",
                            "delivery": "3-5 working day(s)",
                            "price": "8.00",
                            "addon_price": "0.00",
                            "shipment_price": "8.00",
                            "require_min_order": 0,
                            "service_name": "Poslaju Same Day Pick up (within WM)",
                            "courier_name": "POSLAJU NATIONAL COURIER",
                            "dropoff_point": [{
                                "point_id": "EP-CB0MI",
                                "point_name": "Pos Malaysia Banting",
                                "point_contact": "03-3187 1437",
                                "point_addr1": "No. 101 Jalan Bunga, Pekan 2",
                                "point_addr2": "42700",
                                "point_addr3": "",
                                "point_addr4": "",
                                "point_postcode": "Banting",
                                "point_city": "",
                                "point_state": "sgr",
                                "start_time": "00:00:00",
                                "end_time": "00:00:00",
                                "price": 0
                            }],
                            "pickup_point": []
                        },
                        {
                            "rate_id": "EP-RR0MCOV",
                            "service_detail": "pickup",
                            "service_id": "EP-CS0KS",
                            "service_type": "parcel",
                            "courier_id": "EP-CR0Z",
                            "courier_logo": "https://s3-ap-southeast-1.amazonaws.com/easyparcel-static/Public/source/general/img/couriers/CJ_Century.jpg",
                            "scheduled_start_date": "2020-07-21 Tuesday",
                            "pickup_date": "2020-07-21",
                            "delivery": "3-5 working day(s)",
                            "price": "7.80",
                            "addon_price": "0.00",
                            "shipment_price": "7.80",
                            "require_min_order": 0,
                            "service_name": "CJ Century",
                            "courier_name": "CJ Century Logistics Sdn Bhd",
                            "dropoff_point": [],
                            "pickup_point": []
                        },
                        {
                            "rate_id": "EP-RR0914N",
                            "service_detail": "dropoff",
                            "service_id": "EP-CS09J",
                            "service_type": "parcel",
                            "courier_id": "EP-CR0C",
                            "courier_logo": "https://s3-ap-southeast-1.amazonaws.com/easyparcel-static/Public/source/general/img/couriers/DHLeC.jpg",
                            "scheduled_start_date": "2020-07-21 Tuesday",
                            "pickup_date": "2020-07-21",
                            "delivery": "3-5 working day(s)",
                            "price": "7.30",
                            "addon_price": "0.00",
                            "shipment_price": "7.30",
                            "require_min_order": 0,
                            "service_name": "DHL eCommerce (Dropoff only)",
                            "courier_name": "DHL eCommerce",
                            "dropoff_point": [{
                                "point_id": "EP-CB02X",
                                "point_name": "DHL ServicePoint - E3 Farmasi",
                                "point_contact": "",
                                "point_addr1": "71",
                                "point_addr2": "Jalan Bunga Tanjung 6A",
                                "point_addr3": "Taman Muda",
                                "point_addr4": "",
                                "point_postcode": "68000",
                                "point_city": "Ampang",
                                "point_state": "sgr",
                                "start_time": "00:00:00",
                                "end_time": "00:00:00",
                                "price": 0
                            }],
                            "pickup_point": []
                        }
                    ],
                    "pgeon_point": {
                        "Sender_point": [{
                            "point_id": "PGEON_P_TA",
                            "company": "newsplus",
                            "point_name": "TES-S ALAM (43)",
                            "point_contact": "355105643",
                            "point_lat": "3.07191150",
                            "point_lon": "101.53883690",
                            "point_addr1": "LOT 20,1ST FLR TESCO SHAH ALAM,",
                            "point_addr2": "NO 3 JLN AEROBIK 13/43, SEKSYEN 13,",
                            "point_addr3": "",
                            "point_addr4": "",
                            "point_city": "SHAH ALAM",
                            "point_state": "sgr",
                            "point_postcode": "40100",
                            "price": "0.00"
                        }],
                        "Receiver_point": [{
                            "point_id": "PGEON_P_RP",
                            "company": "newsplus",
                            "point_name": "RKL-AMP PARK (271)",
                            "point_contact": "327111975",
                            "point_lat": "3.15987000",
                            "point_lon": "101.71910000",
                            "point_addr1": "AMPANG PARK STATION (UNDERGROUND),",
                            "point_addr2": "JLN AMPANG,",
                            "point_addr3": "",
                            "point_addr4": "",
                            "point_city": "KUALA LUMPUR",
                            "point_state": "kul",
                            "point_postcode": "50450",
                            "price": "0.00"
                        }]
                    }
                }
            ]
        }
