# Copyright (c) 2024, Pritesh Kerai and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from datetime import datetime, timedelta


def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {
            "fieldname": "franchise_name",
            "label": "<b>"+_('Franchise Name')+"</b>",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "fieldname": "no_of_orders",
            "label": "<b>"+_('No of Orders')+"</b>",
            "fieldtype": "Int",
            "width": 125,
        },
        {
            "fieldname": "total_amount",
            "label": "<b>"+_('Total Amount')+"</b>",
            "fieldtype": "Float",
            "width": 125,
        },
    ]

    conditions = []
    params = {}

    if from_date and to_date:
        to_date_end_of_day = (
            datetime.strptime(to_date, "%Y-%m-%d")
            + timedelta(days=1)
            - timedelta(seconds=1)
        )
        conditions.append(
            "o.order_date_time BETWEEN %(from_date)s AND %(to_date_end_of_day)s"
        )
        params["from_date"] = from_date
        params["to_date_end_of_day"] = to_date_end_of_day.strftime("%Y-%m-%d %H:%M:%S")
    elif from_date:
        conditions.append("o.order_date_time >= %(from_date)s")
        params["from_date"] = from_date
    elif to_date:
        to_date_end_of_day = (
            datetime.strptime(to_date, "%Y-%m-%d")
            + timedelta(days=1)
            - timedelta(seconds=1)
        )
        conditions.append("o.order_date_time <= %(to_date_end_of_day)s")
        params["to_date_end_of_day"] = to_date_end_of_day.strftime("%Y-%m-%d %H:%M:%S")

    conditions_str = " AND ".join(conditions)

    query = f"""
        SELECT 
            u.full_name as franchise_name,
            COUNT(o.name) as no_of_orders,
            SUM(o.total_amount) as total_amount
        FROM 
            `tabOrder` o
        JOIN 
            `tabUser` u ON o.user = u.name
        WHERE 
            o.workflow_state IN ('Confirmed', 'Closed')
            AND u.role_profile_name = 'Franchise User'
            {f"AND {conditions_str}" if conditions_str else ""}
        GROUP BY 
            u.full_name
    """

    result = frappe.db.sql(query, params, as_dict=True)

    return columns, result
