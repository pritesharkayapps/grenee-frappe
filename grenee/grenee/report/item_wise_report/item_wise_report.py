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

    columns = [
        {
            "fieldname": "item",
            "label": "<b>" + _("Item") + "</b>",
            "fieldtype": "Data",
            "width": 125,
        },
        {
            "fieldname": "unit",
            "label": "<b>" + _("Unit") + "</b>",
            "fieldtype": "Link",
            "options": "Unit",
            "width": 125,
        },
        {
            "fieldname": "total_sold_qty",
            "label": "<b>" + _("Total Sold Qty") + "</b>",
            "fieldtype": "Int",
            "width": 125,
        },
        {
            "fieldname": "total_amount",
            "label": "<b>" + _("Total Amount") + "</b>",
            "fieldtype": "Float",
            "width": 125,
        },
    ]

    order_filters = {"workflow_state": ["in", ["Confirmed", "Closed"]]}

    if from_date and to_date:
        order_filters["order_date_time"] = ["between", [from_date, to_date]]
    elif from_date:
        order_filters["order_date_time"] = [">=", from_date]
    elif to_date:
        to_date_end_of_day = datetime.strptime(to_date, '%Y-%m-%d') + timedelta(days=1) - timedelta(seconds=1)
        order_filters["order_date_time"] = ["<=", to_date_end_of_day.strftime('%Y-%m-%d %H:%M:%S')]

    orders = frappe.get_all(
        "Order",
        filters=order_filters,
        pluck="name",
    )

    if not orders:
        return columns, []

    query = """
        SELECT 
            oi.item,
            i.unit,
            SUM(ordered_qty) as total_sold_qty,
            SUM(amount) as total_amount
        FROM 
            `tabOrder Items` oi
        JOIN 
            `tabItem` i ON oi.item = i.name
        WHERE 
            parenttype = 'Order' AND
            parent IN (%s)
        GROUP BY 
            item
    """ % ",".join(
        ["%s"] * len(orders)
    )

    result = frappe.db.sql(query, tuple(orders), as_dict=True)

    return columns, result
