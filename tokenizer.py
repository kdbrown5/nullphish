from itsdangerous import URLSafeTimedSerializer
tokenkey = 't$LIJsiogh435t3'
tokensalt = 'I^USFKEUHW#$JKygt'

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(tokenkey)
    return serializer.dumps(email, salt=tokensalt)


def confirm_token(newtoken, expiration=3600):
    serializer = URLSafeTimedSerializer(tokenkey)
    try:
        email = serializer.loads(
            newtoken,
            salt=tokensalt,
            max_age=expiration
        )
    except:
        return False
    return email