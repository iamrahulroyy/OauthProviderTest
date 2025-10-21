from fastapi import APIRouter

from zoho import authorize


router = APIRouter()

router.add_api_route("/authorize", authorize.authorize, methods=["GET"])
router.add_api_route("/callback", authorize.callback, methods=["GET"])
router.add_api_route("/profile", authorize.profile, methods=["GET"])
router.add_api_route("/logout", authorize.logout, methods=["GET"])
