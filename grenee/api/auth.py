import frappe
from werkzeug.wrappers import Response
import json
from grenee.api import helper


@frappe.whitelist(allow_guest=True)
def login(email, password):
    email_exist = frappe.db.exists("User", {"email": email})

    if not email_exist:
        data = {"success": False, "message": "User does not exist with this email."}
        return Response(json.dumps(data), content_type="application/json", status=404)

    try:
        frappe.local.login_manager.authenticate(email, password)

        user_details = frappe.get_doc("User", email)
        api_secret = frappe.generate_hash(length=15)

        if not user_details.api_key:
            user_details.api_key = frappe.generate_hash(length=15)
        user_details.api_secret = api_secret
        user_details.save(ignore_permissions=True)

        frappe.db.commit()

        data = {
            "success": True,
            "message": "Login successful.",
            "user": user_details.as_dict(),
            "token": {
                "api_key": user_details.api_key,
                "api_secret": api_secret,
            },
        }

        return Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
            status=200,
        )
    except frappe.AuthenticationError:
        data = {"success": False, "message": "Invalid password"}
        return Response(json.dumps(data), content_type="application/json", status=401)
    except Exception as e:
        data = {"success": False, "message": str(e)}
        return Response(json.dumps(data), content_type="application/json", status=500)


@frappe.whitelist(methods="GET")
def current_user():
    base_url = frappe.utils.get_url()

    try:
        user_doc = frappe.get_doc("User", frappe.session.user)

        if user_doc.user_image and not user_doc.user_image.startswith(
            ("http://", "https://")
        ):
            user_doc.user_image = f"{base_url}{user_doc.user_image}"

        selected_fields = {
            "email": user_doc.email,
            "full_name": user_doc.full_name,
            "number": user_doc.mobile_no,
            "user_image": user_doc.user_image,
        }

        data = {
            "success": True,
            "message": "User retrieved successfully.",
            "data": selected_fields,
        }

        return Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
            status=200,
        )
    except Exception as e:
        data = {"success": False, "message": str(e)}
        return Response(json.dumps(data), content_type="application/json", status=500)


@frappe.whitelist(methods="GET")
def get_user_slot_status():
    try:
        role_profile_name = frappe.get_value(
            "User", frappe.session.user, "role_profile_name"
        )
        if role_profile_name != "Franchise User":
            error_message = "You are not authorized to access this resource."
            frappe.throw(error_message, title="Unauthorized Access")

        slot = frappe.get_doc("Slot")

        user_slot = frappe.get_value(
            "User Slot",
            {"user": frappe.session.user},
            ["slot", "force_open"],
            as_dict=True,
        )
        
        if not user_slot:
            error_message = "Sorry, there are no available slots for the current user."
            frappe.throw(error_message, title="No Slot Found")

        status = ""

        if user_slot.get("slot") == "Open" or user_slot.get("force_open"):
            status = "Open"
        else:
            status = "Closed"

        data = {"status": status, "slot": slot.as_dict()}

        return Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
            status=200,
        )
    except Exception as e:
        data = {"success": False, "message": str(e)}
        return Response(json.dumps(data), content_type="application/json", status=500)


@frappe.whitelist(methods="GET")
def get_user_slot():
    try:
        role_profile_name = frappe.get_value(
            "User", frappe.session.user, "role_profile_name"
        )
        if role_profile_name != "Franchise User":
            error_message = "You are not authorized to access this resource."
            frappe.throw(error_message, title="Unauthorized Access")

        user_slot = frappe.get_doc("User Slot", {"user": frappe.session.user})

        if not user_slot:
            error_message = "Sorry, there are no available slots for the current user."
            frappe.throw(error_message, title="No Slot Found")

        data = {"success": True, "data": user_slot.as_dict()}

        return Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
            status=200,
        )
    except Exception as e:
        data = {"success": False, "message": str(e)}
        return Response(json.dumps(data), content_type="application/json", status=500)
