import os
from urllib.parse import urlencode

import requests
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter()

META_AUTH_URL = "https://www.facebook.com/dialog/oauth"
META_TOKEN_URL = "https://graph.facebook.com/v20.0/oauth/access_token"
META_ME_ACCOUNTS_URL = "https://graph.facebook.com/v20.0/me/accounts"


@router.get("/auth/instagram/login")
def instagram_login():
    app_id = os.getenv("INSTAGRAM_APP_ID")
    print("INSTAGRAM_APP_ID:", app_id)
    redirect_uri = os.getenv("INSTAGRAM_REDIRECT_URI")

    if not app_id or not redirect_uri:
        raise HTTPException(status_code=500, detail="Instagram env variables are missing")

    params = {
        "client_id": app_id,
        "redirect_uri": redirect_uri,
        "scope": "pages_show_list",
        "response_type": "code",
        "config_id": "1645696583405740",
        "override_default_response_type": "true",
    }

    login_url = f"{META_AUTH_URL}?{urlencode(params)}"
    return RedirectResponse(login_url)


@router.get("/auth/instagram/callback")
def instagram_callback(code: str):
    app_id = os.getenv("INSTAGRAM_APP_ID")
    app_secret = os.getenv("INSTAGRAM_APP_SECRET")
    redirect_uri = os.getenv("INSTAGRAM_REDIRECT_URI")
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:5173")

    if not app_id or not app_secret or not redirect_uri:
        raise HTTPException(status_code=500, detail="Instagram env variables are missing")

    token_params = {
        "client_id": app_id,
        "client_secret": app_secret,
        "redirect_uri": redirect_uri,
        "code": code,
    }

    token_response = requests.get(META_TOKEN_URL, params=token_params)
    token_data = token_response.json()

    if "access_token" not in token_data:
        raise HTTPException(status_code=400, detail=token_data)

    access_token = token_data["access_token"]

    pages_response = requests.get(
        META_ME_ACCOUNTS_URL,
        params={
            "access_token": access_token,
            "fields": "id,name,instagram_business_account",
        },
    )

    pages_data = pages_response.json()

    if "error" in pages_data:
        raise HTTPException(status_code=400, detail=pages_data)

    return RedirectResponse(
        f"{frontend_url}?instagram_connected=true"
    )