# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime,date


def execute(filters=None):
    inv_filters = {}

    start_date_str = filters.get("from_date")
    end_date_str = filters.get("to_date")

    if start_date_str and end_date_str:
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)

        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        inv_filters["invoice_date_time"] = ["between", [start_datetime, end_datetime]]

    if filters.get("user"):
        inv_filters["user"] = filters.get("user")

    columns = get_columns()
    data = []

    invoices = frappe.get_all(
        "Invoice",
        filters=inv_filters,
        fields=["*"],
    )

    for invoice in invoices:
        data.append(
            {
                "date": invoice.invoice_date_time,
                "user": invoice.user,
                "franchise_name": invoice.franchise_name,
                "order": invoice.order,
                "total_amount": invoice.total_amount,
            }
        )

    return columns, data


def get_columns():
    return [
        {
            "fieldname": "date",
            "label": "Invoice Date",
            "fieldtype": "Date",
            "width": 120,
        },
        {
            "fieldname": "user",
            "label": "User",
            "fieldtype": "Link",
            "width": 180,
            "options": "User",
        },
        {
            "fieldname": "franchise_name",
            "label": "Franchise Name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "order",
            "label": "Order",
            "fieldtype": "Link",
            "width": 300,
            "options": "Order",
        },
        {
            "fieldname": "total_amount",
            "label": "Total Amount",
            "fieldtype": "Float",
            "width": 150,
        },
    ]
