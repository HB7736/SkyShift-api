from os import environ

do_exit = False

AWS_ACCESS_KEY = environ.get('AWS_ACCESS_KEY')
if not AWS_ACCESS_KEY:
    print("[!] AWS Access key required")
    # AWS_ACCESS_KEY = 'DEFAULT-Key'
    do_exit = True

AWS_SECRET_KEY = environ.get('AWS_SECRET_KEY')
if not AWS_SECRET_KEY:
    print("[!] AWS Secret required")
    # AWS_SECRET_KEY = 'DEFAULT-Key'
    do_exit = True

API_URL = environ.get('API_URL')
if not API_URL:
    print("[!] API URL required")
    # API_URL = "http://localhost:5000"
    do_exit = True

JENKINS_URL = environ.get('JENKINS_URL')
if not JENKINS_URL:
    print("[!] Jenkins URL required")
    # JENKINS_URL = "http://localhost:8080"
    do_exit = True

USERNAME = environ.get('JENKINS_USERNAME')
if not USERNAME:
    print("[!] Jenkins Username is required")
    # USERNAME = "DEFAULT-username"
    do_exit = True

PASSWORD = environ.get('JENKINS_PASSWORD')
if not PASSWORD:
    print("[!] Jenkins Password or Access Key required")
    # PASSWORD = "DEFAULT-password"
    do_exit = True

if do_exit:
    exit(1)