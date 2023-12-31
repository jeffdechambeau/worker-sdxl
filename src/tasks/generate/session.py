import requests
from requests.adapters import HTTPAdapter, Retry
LOCAL_URL = "http://127.0.0.1:3000"
LOCAL_URL = "https://a8lbi00mdlwpal-3001.proxy.runpod.net"

automatic_session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
automatic_session.mount('http://', HTTPAdapter(max_retries=retries))
