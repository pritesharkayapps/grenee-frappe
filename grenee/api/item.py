import frappe
from grenee.api import helper
import json


@frappe.whitelist()
def all_categories():
    try:
        categories = frappe.get_list(
            "Category",
            fields=["*"],
            ignore_permissions=True,
        )

        data = {
            "success": True,
            "message": "Categories Retrieved Successfully.",
            "data": categories,
        }

        return helper.response(data, 200)
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response


@frappe.whitelist()
def all_items():
    try:
        items = frappe.get_list("Item", filters={"disabled": False}, fields=["*"])

        data = {
            "success": True,
            "message": "Items Retrieved Successfully.",
            "data": items,
        }

        return helper.response(data, 200)
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response


@frappe.whitelist()
def get_items(filters=None):
    try:
        filters_dict = {"disabled": False}
        if filters:
            parsed_filters = frappe.parse_json(filters)
            filters_dict.update(parsed_filters)

        items = frappe.get_list("Item", filters=filters_dict, fields=["*"])

        data = {
            "success": True,
            "message": "Items Retrieved Successfully.",
            "data": items,
        }

        return helper.response(data, 200)
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response
