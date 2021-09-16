from suds.client import Client


def zarrinpal_request_handler(amount, description, user_email, user_phone_number, REQUEST_URL, MERCHANT_ID, CALL_BACK):
    client = Client(REQUEST_URL)
    result = client.service.PaymentRequest(
        MERCHANT_ID, amount, description, user_email, user_phone_number, CALL_BACK
    )
    if result.Status == 100:
        return 'https://sandbox.zarinpal.com/pg/StartPay/' + result.Authority, result.Authority
    else:
        return None, None


def zarrinpal_payment_verify(amount, authority, REQUEST_URL, MERCHANT_ID,):
    client = Client(REQUEST_URL)
    result = client.service.PaymentVerification(MERCHANT_ID, authority, amount)
    is_paid = True if result.Status in (100, 101) else False
    return is_paid, result.RefID
