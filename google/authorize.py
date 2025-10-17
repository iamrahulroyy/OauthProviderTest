import os
from authlib.integrations.starlette_client import OAuth, OAuthError
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

router = APIRouter()

# --- OAuth Configuration ---
oauth = OAuth()

google_client_id = os.getenv("GOOGLE_CLIENT_ID")
google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")

if not google_client_id or not google_client_secret:
    raise ValueError("GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET must be set in your environment variables.")

oauth.register(
    name='google',
    client_id=google_client_id,
    client_secret=google_client_secret,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# --- Routes ---

@router.get('/authorize')
async def authorize(request: Request):
    """
    Redirects the user to Google's authorization page.
    """
    redirect_uri = request.url_for('callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/callback')
async def callback(request: Request):
    """
    Handles the callback from Google after user authorization.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
    except OAuthError as error:
        return JSONResponse(
            status_code=400,
            content={'error': 'Failed to get access token', 'details': error.description}
        )

    # Use the userinfo endpoint to get user details. This is more robust.
    user_info = await oauth.google.userinfo(token=token)

    if user_info:
        # In a real app, you would find or create a user in your database here
        # and then store your internal user ID in the session.
        request.session['user'] = dict(user_info)

    return RedirectResponse(url='/provider/google/profile')

@router.get('/profile')
async def profile(request: Request):
    """
    A protected route that displays user information from the session.
    """
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/provider/google/authorize')
    return JSONResponse(user)

@router.get('/logout')
async def logout(request: Request):
    """
    Clears the user session.
    """
    request.session.pop('user', None)
    return RedirectResponse(url='/')

