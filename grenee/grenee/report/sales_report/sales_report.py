import frappe
from frappe import _


def execute(filters=None):
    if not filters:
        filters = {}

    from_date = filters.get("from_date")
    to_date = filters.get("to_date")

    columns = [
        {
            "fieldname": "order_date",
            "label": "<b>" + _("Order Date") + "</b>",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "fieldname": "no_of_orders",
            "label": "<b>" + _("No of Orders") + "</b>",
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

    # Prepare SQL conditions for date filters
    conditions = []
    if from_date:
        conditions.append("o.order_date_time >= %(from_date)s")
    if to_date:
        conditions.append("o.order_date_time < DATE_ADD(%(to_date)s, INTERVAL 1 DAY)")

    conditions_str = " AND ".join(conditions)

    # Construct SQL query
    query = f"""
        SELECT 
            DATE(o.order_date_time) as order_date,
            COUNT(o.name) as no_of_orders,
            SUM(o.total_amount) as total_amount
        FROM 
            `tabOrder` o
        WHERE 
            o.workflow_state IN ('Confirmed', 'Closed')
            {f"AND {conditions_str}" if conditions_str else ""}
        GROUP BY 
            DATE(o.order_date_time)
        ORDER BY 
            DATE(o.order_date_time)
    """

    # Execute SQL query
    result = frappe.db.sql(query, filters, as_dict=True)

    return columns, result
