# Google OAuth2 Credentials:

Go to the Google API Console.

Create a new project.

Go to the "OAuth consent screen" and configure it.

Go to "Credentials", click "Create Credentials", and select "OAuth client ID".

Choose "Web application" as the application type.

Under "Authorized redirect URIs", add http://127.0.0.1:8000/provider/google/callback.

You will get a Client ID and a Client Secret.

Environment Variables:
Create a file named .env in the root of your project and add your Google credentials:

GOOGLE_CLIENT_ID=YOUR_GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET=YOUR_GOOGLE_CLIENT_SECRET

Then try the login flow again in your browser by going to http://127.0.0.1:8000/provider/google/authorize.



# Zoho setup

Go to the Zoho API Console.

Click GET STARTED.

Select Server-based Applications.

Provide a Client Name (e.g., "My SSO App").

For the Homepage URL, enter http://127.0.0.1:8000.`

For the Authorized Redirect URI, enter http://127.0.0.1:8000/provider/zoho/callback.

Click CREATE.

You will be taken to a page with your Client ID and Client Secret.

# Zoho Credentials
ZOHO_CLIENT_ID=YOUR_ZOHO_CLIENT_ID
ZOHO_CLIENT_SECRET=YOUR_ZOHO_CLIENT_SECRET