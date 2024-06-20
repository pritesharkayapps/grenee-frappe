# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime
import pytz


class Order(Document):
    def validate(self):
        self.validate_order_qty()

    def validate_order_qty(self):
        for item in self.order_items:
            if item.ordered_qty < item.min_qty:
                frappe.throw(
                    f"Order quantity cannot be less than the minimum quantity for row {item.idx}"
                )

            if item.ordered_qty > item.max_qty:
                frappe.throw(
                    f"Order quantity cannot exceed the maximum quantity for row {item.idx}"
                )

            if item.ordered_qty % item.lot_qty != 0:
                frappe.throw(
                    f"Order quantity must be a multiple of the lot size for row {item.idx}"
                )
