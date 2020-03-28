from itsdangerous import URLSafeTimedSerializer
tokenkey = 't$LIJsiogh435t3'
tokensalt = 'I^USFKEUHW#$JKygt'

def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(tokenkey)
    return serializer.dumps(email, salt=tokensalt)


def confirm_token(newtoken, expiration=3600):# one hour
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

def confirm_15mtoken(newtoken, expiration=900):# one hour
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

def confirm_twoweektoken(newtoken, expiration=2419200):# 2 weeks
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