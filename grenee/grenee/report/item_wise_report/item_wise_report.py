# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {
            "fieldname": "item",
            "label": ("Item"),
            "fieldtype": "Data",
            "width": 125,
        },
        {
            "fieldname": "unit",
            "label": ("Unit"),
            "fieldtype": "Link",
            "options": "Unit",
            "width": 125,
        },
        {
            "fieldname": "total_sold_qty",
            "label": ("Total Sold Qty"),
            "fieldtype": "Int",
            "width": 125,
        },
        {
            "fieldname": "total_price",
            "label": ("Total Price"),
            "fieldtype": "Float",
            "width": 125,
        },
    ]

    items = frappe.get_all("Item", filters={"disabled": False}, fields=["*"])

    datas = []

    for item in items:
        order_items = frappe.get_all(
            "Order Items",
            filters={"item": item.name, "parenttype": "Order", "docstatus": 1},
            fields=["ordered_qty", "amount"],
        )

        sold_qty = 0
        sold_amount = 0
        for order_item in order_items:
            sold_qty += order_item["ordered_qty"]
            sold_amount += order_item["amount"]

        datas.append(
            {
                "item": item.item_name,
                "total_sold_qty": sold_qty,
                "unit": item.unit,
                "total_price": sold_amount,
            }
        )

    return columns, datas
