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

zoho_client_id = os.getenv("ZOHO_CLIENT_ID")
zoho_client_secret = os.getenv("ZOHO_CLIENT_SECRET")

if not zoho_client_id or not zoho_client_secret:
    # This check is important, but we'll allow the app to start
    # so the developer can see the instructions.
    print("Warning: ZOHO_CLIENT_ID and ZOHO_CLIENT_SECRET are not set.")

oauth.register(
    name='zoho',
    client_id=zoho_client_id,
    client_secret=zoho_client_secret,
    access_token_url='https://accounts.zoho.com/oauth/v2/token',
    authorize_url='https://accounts.zoho.com/oauth/v2/auth',
    api_base_url='https://accounts.zoho.com/oauth/user/info',
    client_kwargs={'scope': 'AaaServer.profile.READ'}
)

# --- Routes ---

@router.get('/authorize')
async def authorize(request: Request):
    """
    Redirects the user to Zoho's authorization page.
    """
    if not zoho_client_id or not zoho_client_secret:
        return JSONResponse(
            status_code=500,
            content={"error": "Zoho credentials not configured on the server."}
        )
    redirect_uri = request.url_for('callback')
    return await oauth.zoho.authorize_redirect(request, redirect_uri)

@router.get('/callback')
async def callback(request: Request):
    """
    Handles the callback from Zoho after user authorization.
    """
    try:
        token = await oauth.zoho.authorize_access_token(request)
    except OAuthError as error:
        return JSONResponse(
            status_code=400,
            content={'error': 'Failed to get access token', 'details': error.description}
        )

    # Use the userinfo endpoint to get user details.
    resp = await oauth.zoho.get('', token=token)
    user_info = resp.json()

    if user_info:
        # In a real app, you would find or create a user in your database here
        # and then store your internal user ID in the session.
        request.session['user'] = user_info

    return RedirectResponse(url='/provider/zoho/profile')

@router.get('/profile')
async def profile(request: Request):
    """
    A protected route that displays user information from the session.
    """
    user = request.session.get('user')
    if not user:
        return RedirectResponse(url='/provider/zoho/authorize')
    return JSONResponse(user)

@router.get('/logout')
async def logout(request: Request):
    """
    Clears the user session.
    """
    request.session.pop('user', None)
    return RedirectResponse(url='/')
