from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.http import HttpResponse
from realex.realex import Realex

Realex.REALEX_SHARED_SECRET = settings.REALEX_SHARED_SECRET
Realex.REALEX_URL = settings.REALEX_URL
Realex.REALEX_MERCHANT_ID = settings.REALEX_MERCHANT_ID


@require_http_methods(['GET'])
def main(request):
    return render(request, "index.html")


@require_http_methods(['POST'])
def donations(request):
    response = Realex.create_charge(
        amount=request.POST['amount'],
        currency=request.POST['currency'],
        card_holder_name=request.POST['card_holder_name'],
        card_number=request.POST['card_number'],
        cvv=request.POST['cvv'],
        expiry_month=request.POST['expiry_month'],
        expiry_year=request.POST['expiry_year'],
        card_type=request.POST['card_type']
    )

    http_response = HttpResponse(response['message'], content_type="text/plain")
    http_response.status_code = response['status_code']
    http_response['realex_result_code'] = response['realex_result_code']
    return http_response

