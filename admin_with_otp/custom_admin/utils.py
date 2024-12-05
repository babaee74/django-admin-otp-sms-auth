import requests
from admin_with_otp.settings import OTP_SERVICE_URL, MAX_OTP_TRIES

def get_otp_code(mobile):
    attempts = 0
    code = None
    data = {'to': mobile}

    while 1:
        response = requests.post(OTP_SERVICE_URL, json=data)
        if response.status_code==200:
            resp_data = response.json()
            code = resp_data.get("code", None)
        if code is not None:
            break
        else:
            if attempts>=MAX_OTP_TRIES:
                break
        attempts += 1
    return code