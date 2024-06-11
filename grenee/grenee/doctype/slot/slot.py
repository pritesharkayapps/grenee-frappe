# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime
from datetime import datetime
from frappe.model.workflow import apply_workflow


class Slot(Document):
    pass


def update_user_slot():
    current_time = now_datetime().time().replace(microsecond=0)

    get_slot = frappe.get_single("Slot")
    start_time = datetime.strptime(get_slot.start_time, "%H:%M:%S").time()
    end_time = datetime.strptime(get_slot.end_time, "%H:%M:%S").time()

    count_open_slot = frappe.db.count("User Slot", filters={"slot": "Open"})
    count_closed_slot = frappe.db.count("User Slot", filters={"slot": "Closed"})

    if start_time < end_time:
        print("open_slot",count_open_slot)
        print("count_closed_slot",count_closed_slot)
        print((start_time <= current_time < end_time) and count_open_slot > 0)

        if (start_time <= current_time < end_time):
            slots = frappe.get_all("User Slot", filters={"slot": "Closed"})
            for slot in slots:
                user_slot = frappe.get_doc("User Slot", slot.name)
                user_slot.slot = "Open"
                user_slot.save()
        else:
            slots = frappe.get_all("User Slot", filters={"slot": "Open"})
            for slot in slots:
                user_slot = frappe.get_doc("User Slot", slot.name)
                user_slot.slot = "Closed"
                user_slot.save()
    else:
        if (start_time <= current_time or current_time < end_time):
            slots = frappe.get_all("User Slot", filters={"slot": "Closed"})
            for slot in slots:
                user_slot = frappe.get_doc("User Slot", slot.name)
                user_slot.slot = "Open"
                user_slot.save()
        else:
            slots = frappe.get_all("User Slot", filters={"slot": "Open"})
            for slot in slots:
                user_slot = frappe.get_doc("User Slot", slot.name)
                user_slot.slot = "Closed"
                user_slot.save()

        frappe.db.commit()


def update_order_status():
    try:
        user_slots = frappe.get_all("User Slot", fields=["*"])

        for user_slot in user_slots:
            total_open_order = frappe.db.count(
                "Order", filters={"user": user_slot.user, "workflow_state": "Open"}
            )
            total_confirmed_order = frappe.db.count(
                "Order",
                filters={"user": user_slot.user, "workflow_state": "Confirmed"},
            )

            if (
                user_slot.slot == "Closed" and user_slot.force_open == False
            ) and total_open_order > 0:
                orders = frappe.get_all("Order", filters={"workflow_state": "Open"})
                for order in orders:
                    order_doc = frappe.get_doc("Order", order.name)
                    apply_workflow(order_doc, "Confirm")

                    frappe.db.commit()

            if user_slot.slot == "Open" and total_confirmed_order > 0:
                orders = frappe.get_all(
                    "Order", filters={"workflow_state": "Confirmed"}
                )
                for order in orders:
                    order_doc = frappe.get_doc("Order", order.name)
                    apply_workflow(order_doc, "Close")

                    frappe.db.commit()

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in Confirming Order")
        frappe.db.rollback()
