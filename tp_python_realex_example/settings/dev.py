from tp_python_realex_example.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", "mq(v8&i$ua(a&_@@$kd*7dglot32bbs7#nu*o77g^88+q(wpv3")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

REALEX_URL = "https://api.testingpays.com/realex/v1/auth"
REALEX_VERIFY_SIGNED_URL = os.environ.get("REALEX_VERIFY_SIGNED_URL",
                                          "https://api.testingpays.com/realex/v1/3ds_verifysig")
REALEX_VERIFY_ENROLLED_URL = os.environ.get("REALEX_VERIFY_ENROLLED_URL",
                                            "https://api.testingpays.com/realex/v1/3ds_verifyenrolled")
REALEX_CALLBACK_URL = os.environ.get("REALEX_CALLBACK_URL", "http://127.0.0.1:8000/threedsverifysig")
REALEX_MERCHANT_ID = os.environ.get("REALEX_MERCHANT_ID", "<insert-your-realex-id-here>")
REALEX_SHARED_SECRET = os.environ.get("REALEX_SHARED_SECRET", "<insert-your-realex-shared-secret-key-here>")

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
