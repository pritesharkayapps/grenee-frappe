# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime,timedelta


def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = get_columns()
    data = []

    inv_filters = {"docstatus": 1}

    if from_date and to_date:
        inv_filters["invoice_date_time"] = ["between", [from_date, to_date]]
    elif from_date:
        inv_filters["invoice_date_time"] = [">=", from_date]
    elif to_date:
        to_date_end_of_day = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        inv_filters["invoice_date_time"] = ["<=", to_date_end_of_day.strftime('%Y-%m-%d %H:%M:%S')]

    if filters.get('user'):
        inv_filters["user"] = filters.get('user')

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
