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

        selected_fields = {
            "email": user_doc.email,
            "full_name": user_doc.full_name,
            "number": user_doc.mobile_no,
            "user_image": (
                f"{base_url}{user_doc.user_image}" if user_doc.user_image else None
            ),
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
        if (
            frappe.get_value("User", frappe.session.user, "role_profile_name")
            != "Franchise User"
        ):
            frappe.throw(
                ("You are not authorized to access this resource."),
                title="Unauthorized Access",
            )

        user_slot = frappe.get_value(
            "User Slot",
            {"user": frappe.session.user},
            ["slot", "force_open"],
            as_dict=True,
        )

        if not user_slot:
            frappe.throw(
                ("No user slot found for the current user."), title="No Slot Found"
            )

        return (
            "Open"
            if user_slot.get("slot") == "Open" or user_slot.get("force_open")
            else "Closed"
        )
    except Exception as e:
        data = {"success": False, "message": str(e)}
        return Response(json.dumps(data), content_type="application/json", status=500)
