# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Item(Document):
    def validate(self):
        self.validate_min_max_qty()

    def validate_min_max_qty(self):
        if self.min_qty < self.lot_qty:
            frappe.throw(f"Minimum Quantity should not be less than Lot Quantity.")

        if self.max_qty < self.lot_qty:
            frappe.throw(f"Maximum Quantity should not be less than Lot Quantity.")

        if self.min_qty % self.lot_qty != 0:
            frappe.throw(f"Minimum Quantity should be a multiple of Lot Quantity.")

        if self.max_qty % self.lot_qty != 0:
            frappe.throw(f"Maximum Quantity should be a multiple of Lot Quantity.")
