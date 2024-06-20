# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Item(Document):
    def validate(self):
        self.validate_min_max_qty()

    def on_update(self):
        has_open_slot = (
            frappe.db.exists("User Slot", {"slot": "Open"}) or 
            frappe.db.exists("User Slot", {"force_open": 1})
        )

        if has_open_slot:
            frappe.throw("You can Update Item After All User Slots are Closed")

    def validate_min_max_qty(self):
        if self.min_qty < self.lot_qty:
            frappe.throw("Minimum Quantity should not be less than Lot Quantity.")

        if self.max_qty < self.lot_qty:
            frappe.throw("Maximum Quantity should not be less than Lot Quantity.")

        if self.min_qty % self.lot_qty != 0:
            frappe.throw("Minimum Quantity should be a multiple of Lot Quantity.")

        if self.max_qty % self.lot_qty != 0:
            frappe.throw("Maximum Quantity should be a multiple of Lot Quantity.")
