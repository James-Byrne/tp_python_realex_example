from datetime import datetime
import hashlib
import xmltodict
import os
import requests
from realex.lib import *
import re

BASE_DIR = os.path.dirname(os.path.abspath('realex_auth.py'))
_RELATIVE_LOCATION_TO_BASE_XML_FILE = '/realex/realex_files/realex_auth.xml'
_REALEX_ORDERID_LENGTH = 13


class Realex:
    REALEX_SHARED_SECRET = None
    REALEX_URL = None
    REALEX_MERCHANT_ID = None

    @classmethod
    def create_charge(cls, amount, currency, card_holder_name, card_number, cvv, expiry_month, expiry_year, card_type):
        verify_constants_are_configured(cls.REALEX_SHARED_SECRET, cls.REALEX_URL, cls.REALEX_MERCHANT_ID)

        response = requests.post(cls.REALEX_URL,
                                 data=_generate_xml_data(remove_decimal_places(amount),
                                                         currency,
                                                         card_holder_name,
                                                         remove_white_space(card_number),
                                                         cvv,
                                                         expiry_month,
                                                         expiry_year,
                                                         card_type,
                                                         cls.REALEX_MERCHANT_ID,
                                                         cls.REALEX_SHARED_SECRET),
                                 headers=generate_basic_xml_headers())
        return parse_realex_response(response)


def verify_constants_are_configured(shared_secret, url, merchant_id):
    if not shared_secret:
        raise ValueError('REALEX_SHARED_SECRET must be configured')
    if not url:
        raise ValueError('REALEX_URL must be configured')
    if not merchant_id:
        raise ValueError('REALEX_MERCHANT_ID must be configured')


def _generate_xml_data(amount, currency, card_holder_name, card_number, cvv, expiry_month, expiry_year, card_type,
                       realex_merchant_id, shared_secret):
    untangled_xml = _get_untangled_base_xml()

    _update_untangled_xml(amount, card_holder_name, card_number, card_type, currency, cvv, expiry_month, expiry_year,
                          _generate_orderid(), realex_merchant_id, shared_secret, _generate_time_stamp(), untangled_xml)

    return _convert_to_xml(untangled_xml)


def parse_realex_response(response):
    realex_result_code = extract_xml_response_from_realex(response)['result']
    realex_message = extract_xml_response_from_realex(response)['message']

    if realex_result_code == '00':
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code, 'message': 'SUCCESS'}
    elif realex_result_code == '101':
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code,
                'message': realex_message}
    elif re.search(r'^10[2,3,7]', realex_result_code):
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code, 'message': 'DECLINED'}
    elif re.search(r'^2[0-9][0-9]', realex_result_code):
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code, 'message': 'BANK_ERROR'}
    elif re.search(r'^3[0-9][0-9]', realex_result_code):
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code,
                'message': 'REALEX_ERROR'}
    elif re.search(r'^5[0-9][0-9]', realex_result_code):
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code,
                'message': realex_message}
    elif re.search(r'^60[0,1,3]', realex_result_code):
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code, 'message': 'ERROR'}
    elif realex_result_code == '666':
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code,
                'message': 'CLIENT_DEACTIVATED'}
    else:
        return {'status_code': response.status_code, 'realex_result_code': realex_result_code, 'message': 'NOT FOUND'}


def extract_xml_response_from_realex(custom_response):
    return xmltodict.parse(custom_response.content)['response']


def _update_untangled_xml(amount, card_holder_name, card_number, card_type, currency, cvv, expiry_month, expiry_year,
                          orderid, realex_merchant_id, shared_secret, timestamp, untangled_xml):
    _set_sha1hash(amount, card_number, currency, orderid, realex_merchant_id, timestamp, untangled_xml, shared_secret)
    _set_orderid(orderid, untangled_xml)
    _set_timestamp(timestamp, untangled_xml)
    _set_amount_and_currency(amount, currency, untangled_xml)
    _set_card_number(card_number, untangled_xml)
    _set_card_holder_name(card_holder_name, untangled_xml)
    _set_cvv(cvv, untangled_xml)
    _set_expiry_month_and_year(expiry_month, expiry_year, untangled_xml)
    _set_card_type(card_type, untangled_xml)
    _set_merchant_id(realex_merchant_id, untangled_xml)


def _set_sha1hash(amount, card_number, currency, orderid, realex_merchant_id, timestamp, untangled_xml, shared_secret):
    untangled_xml['request']['sha1hash'] = _generate_sha1hash(timestamp, realex_merchant_id, orderid,
                                                              amount, currency, card_number,
                                                              shared_secret)


def _generate_orderid():
    return generate_random_alphanumeric_string(_REALEX_ORDERID_LENGTH)


def _generate_sha1hash(timestamp, realex_merchant_id, orderid, amount, currency, card_number, shared_secret):
    initial_sha1_hash = hashlib.sha1((timestamp + realex_merchant_id + orderid + amount + currency + card_number)
                                     .encode('utf-8')).hexdigest()

    return hashlib.sha1((initial_sha1_hash + "." + shared_secret).encode('utf-8')).hexdigest()


def _set_orderid(orderid, untangled_xml):
    untangled_xml['request']['orderid'] = orderid


def _set_timestamp(timestamp, untangled_xml):
    untangled_xml['request']['@timestamp'] = timestamp


def _generate_time_stamp():
    return "{:%Y%m%d%H%M%S}".format(datetime.now())


def _set_merchant_id(realex_merchant_id, untangled_xml):
    untangled_xml['request']['merchantid'] = realex_merchant_id


def _set_card_type(card_type, untangled_xml):
    untangled_xml['request']['card']['type'] = card_type


def _set_expiry_month_and_year(expiry_month, expiry_year, untangled_xml):
    untangled_xml['request']['card']['expdate'] = expiry_month + expiry_year


def _set_cvv(cvv, untangled_xml):
    untangled_xml['request']['card']['cvn']['number'] = cvv


def _set_card_holder_name(card_holder_name, untangled_xml):
    untangled_xml['request']['card']['chname'] = card_holder_name


def _set_card_number(card_number, untangled_xml):
    untangled_xml['request']['card']['number'] = card_number


def _set_amount_and_currency(amount, currency, untangled_xml):
    untangled_xml['request']['amount']['#text'] = amount
    untangled_xml['request']['amount']['@currency'] = currency


def _get_untangled_base_xml():
    with open(_get_xml_file_location()) as fd:
        untangled_xml = xmltodict.parse(fd.read())
    return untangled_xml


def _convert_to_xml(untangled_xml):
    return xmltodict.unparse(untangled_xml, full_document=False)


def _get_xml_file_location():
    return BASE_DIR + _RELATIVE_LOCATION_TO_BASE_XML_FILE
