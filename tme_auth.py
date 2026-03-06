import base64
import hashlib
import hmac
import logging
import os
from urllib.parse import quote, urlencode

import requests
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

API_BASE = "https://api.tme.eu"

TME_APP_TOKEN = os.getenv("TME_APP_TOKEN", "")
TME_APP_SECRET = os.getenv("TME_APP_SECRET", "")
TME_COUNTRY = os.getenv("TME_COUNTRY", "PL")
TME_LANGUAGE = os.getenv("TME_LANGUAGE", "EN")
TME_CURRENCY = os.getenv("TME_CURRENCY", "PLN")


def _sign_request(url: str, params: dict) -> dict:
    """Sign a TME API request using HMAC-SHA1.

    Returns the params dict with Token and ApiSignature added.
    """
    params["Token"] = TME_APP_TOKEN

    # 1. Sort params alphabetically by key
    sorted_params = sorted(params.items())

    # 2. Build signature base string: POST&url_encoded&params_encoded
    encoded_url = quote(url, safe="")
    # Use quote (RFC 3986 %20) not urlencode default (+) — TME uses rawurlencode
    encoded_params = quote(urlencode(sorted_params, quote_via=quote), safe="")
    signature_base = f"POST&{encoded_url}&{encoded_params}"

    # 3. HMAC-SHA1 with app secret, then base64
    signature = hmac.new(
        TME_APP_SECRET.encode("utf-8"),
        signature_base.encode("utf-8"),
        hashlib.sha1,
    )
    params["ApiSignature"] = base64.b64encode(signature.digest()).decode("utf-8")

    return params


def _make_request(endpoint: str, params: dict | None = None) -> dict:
    """Make a signed POST request to the TME API.

    Args:
        endpoint: API endpoint path (e.g. "Products/Search")
        params: Additional request parameters (without Token/ApiSignature)

    Returns:
        Parsed JSON response data.
    """
    if not TME_APP_TOKEN or not TME_APP_SECRET:
        raise ValueError("TME_APP_TOKEN and TME_APP_SECRET must be set")

    url = f"{API_BASE}/{endpoint}.json"
    body = dict(params) if params else {}
    body["Country"] = TME_COUNTRY
    body["Language"] = TME_LANGUAGE

    signed_body = _sign_request(url, body)

    logger.info(f"POST {url}")
    resp = requests.post(url, data=signed_body, timeout=30)

    data = resp.json()

    if resp.status_code != 200:
        msg = data.get("ErrorMessage", "")
        detail = data.get("Error", "")
        raise RuntimeError(f"TME API error ({resp.status_code}): {msg} {detail}".strip())

    if data.get("Status") != "OK":
        error = data.get("Error", "Unknown error")
        raise RuntimeError(f"TME API error: {error}")

    return data.get("Data", data)
