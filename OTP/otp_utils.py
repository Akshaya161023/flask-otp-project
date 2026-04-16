import hmac, hashlib, time

SECRET_KEY = "your_secret_key_here"
OTP_VALIDITY = 300  # 5 minutes

def generate_otp(email):
    window = int(time.time()) // OTP_VALIDITY
    message = f"{email}{window}".encode()
    digest = hmac.new(SECRET_KEY.encode(), message, hashlib.sha256).hexdigest()
    return digest[:6].upper()

def verify_otp(email, user_input):
    expected = generate_otp(email)
    return hmac.compare_digest(expected, user_input.strip().upper())