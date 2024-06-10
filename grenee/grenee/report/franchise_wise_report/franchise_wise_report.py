# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {
            "fieldname": "franchise_name",
            "label": ("Franchise Name"),
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "no_of_orders",
            "label": ("No of Orders"),
            "fieldtype": "Int",
            "width": 125,
        },
        {
            "fieldname": "total_amount",
            "label": ("Total Amount"),
            "fieldtype": "Float",
            "width": 125,
        },
    ]

    franchise_users = frappe.get_all("User", filters={"role_profile_name":'Franchise User'}, fields=["*"])

    datas = []

    for franchise_user in franchise_users:
        invoices = frappe.get_all(
            "Invoice",
            filters={"user": franchise_user.name, "docstatus": 1},
            fields=["*"]
        )

        total_amount = 0
        for invoice in invoices:
            total_amount += invoice.total_amount

        datas.append(
            {
                "franchise_name": franchise_user.full_name,
                "no_of_orders": len(invoices),
                "total_amount": total_amount,
            }
        )

    return columns, datas
