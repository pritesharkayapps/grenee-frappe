import frappe
from werkzeug.wrappers import Response
import json
from grenee.api import helper
import pytz
from datetime import datetime


@frappe.whitelist(methods="POST")
def place_order(**kwargs):
    payload = frappe.parse_json(kwargs)

    try:
        user_slot = frappe.get_value(
            "User Slot",
            {"user": frappe.session.user},
            ["slot", "force_open"],
            as_dict=True,
        )

        if user_slot.get("slot") == "Closed" and user_slot.get("force_open") == False:
            frappe.throw("ORDER SLOTS CLOSED")

        order_items, total_amount = get_order_items_and_total(payload.get("items", []))

        order = create_order(order_items, total_amount)
        order.save()
        frappe.db.commit()

        data = {
            "success": True,
            "message": "Your Order has been Placed.",
            "data": order.as_dict(),
        }
        response = Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
        )

        return response
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = Response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response


def get_order_items_and_total(items):
    order_items = []
    total_amount = 0

    for item in items:
        item_doc = frappe.get_doc("Item", item["item_id"])
        ordered_qty = item["ordered_qty"]
        amount = item_doc.price_per_unit * ordered_qty

        order_items.append(
            {
                "category": item_doc.category,
                "item": item_doc.name,
                "unit": item_doc.unit,
                "lot_qty": item_doc.lot_qty,
                "min_qty": item_doc.min_qty,
                "max_qty": item_doc.max_qty,
                "rate": item_doc.price_per_unit,
                "ordered_qty": ordered_qty,
                "amount": amount,
            }
        )

        total_amount += amount

    return order_items, total_amount


def create_order(order_items, total_amount):
    order = frappe.new_doc("Order")
    order.user = frappe.session.user
    order.total_amount = total_amount
    order.order_date_time = get_current_datetime_in_india()

    for item in order_items:
        order.append(
            "order_items",
            {
                "item": item["item"],
                "category": item["category"],
                "unit": item["unit"],
                "lot_qty": item["lot_qty"],
                "min_qty": item["min_qty"],
                "max_qty": item["max_qty"],
                "rate": item["rate"],
                "ordered_qty": item["ordered_qty"],
                "amount": item["amount"],
            },
        )

    return order


def get_current_datetime_in_india():
    india_tz = pytz.timezone("Asia/Kolkata")
    return datetime.now(india_tz).strftime("%Y-%m-%d %H:%M:%S")


@frappe.whitelist(methods="GET")
def get_order(id):
    try:
        order = frappe.get_doc("Order", id)

        if order.user != frappe.session.user:
            frappe.throw("You are not the owner of this Order.")

        order_dict = order.as_dict()

        for item in order_dict.order_items:
            item_doc = frappe.get_doc("Item", item.item)
            item.item_doc = item_doc.as_dict()

        data = {
            "success": True,
            "message": "Order Retrieved Successfully.",
            "data": order_dict,
        }

        response = Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
        )

        return response
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = Response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response


@frappe.whitelist(methods="POST")
def update_order(id, **kwargs):
    payload = frappe.parse_json(kwargs)

    try:
        order = frappe.get_doc("Order", id)

        if order.user != frappe.session.user:
            frappe.throw("You are not the owner of this order.")

        user_slot = frappe.get_value(
            "User Slot",
            {"user": frappe.session.user},
            ["slot", "force_open"],
            as_dict=True,
        )

        if user_slot.get("slot") == "Closed" and user_slot.get("force_open") == False:
            frappe.throw("ORDER SLOTS CLOSED")

        order.order_items = []
        order_items, total_amount = get_order_items_and_total(payload.get("items", []))
        order.total_amount = total_amount

        for item in order_items:
            order.append("order_items", item)
        order.save()

        frappe.db.commit()

        data = {
            "success": True,
            "message": "Order Updated Successfully.",
            "data": order.as_dict(),
        }

        response = Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
        )
        return response
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = Response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response


@frappe.whitelist(methods="GET")
def delete_order(id):
    try:
        order_doc = frappe.get_doc("Order", id)

        if order_doc.user != frappe.session.user:
            frappe.throw("You are not the owner of this Order.")

        user_slot = frappe.get_value(
            "User Slot",
            {"user": frappe.session.user},
            ["slot", "force_open"],
            as_dict=True,
        )

        if user_slot.get("slot") == "Closed" and user_slot.get("force_open") == False:
            frappe.throw("ORDER SLOTS CLOSED")

        frappe.delete_doc("Order", id)
        frappe.db.commit()

        data = {"success": True, "message": "Your Order has been Deleted"}

        response = Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
        )

        return response
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = Response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response


@frappe.whitelist(methods="GET")
def get_active_orders():
    try:
        orders = frappe.get_list(
            "Order",
            filters={
                "user": frappe.session.user,
                "workflow_state": ["in", ["Open", "Confirmed"]],
            },
            fields=["*"],
        )

        data = {
            "success": True,
            "message": "Active Orders Retrieved Successfully.",
            "data": orders,
        }

        response = Response(
            json.dumps(data, cls=helper.CustomJSONEncoder),
            content_type="application/json",
        )

        return response
    except Exception as e:
        data = {"success": False, "message": str(e)}

        response = Response(json.dumps(data), content_type="application/json")
        response.status_code = 500
        return response
