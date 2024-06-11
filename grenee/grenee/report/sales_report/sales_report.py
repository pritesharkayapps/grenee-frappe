import frappe
from datetime import datetime, timedelta

def execute(filters=None):
    if not filters:
        filters = {}

    start_date_str = filters.get("from_date")
    end_date_str = filters.get("to_date")

    if not start_date_str or not end_date_str:
        frappe.throw("Please specify both 'from_date' and 'to_date' filters.")

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    # Ensure start_date is not after end_date
    if start_date > end_date:
        frappe.throw("'from_date' cannot be after 'to_date'.")

    columns = get_columns()

    date_list = generate_date_list(start_date, end_date)

    data = []

    for date in date_list:
        start_datetime = datetime.combine(date, datetime.min.time())
        end_datetime = datetime.combine(date, datetime.max.time())
        
        invoices = frappe.get_all(
            "Order",
            filters={"order_date_time": ["between", [start_datetime, end_datetime]],'docstatus':1},
            fields=["total_amount"]
        )

        total_amount = sum(float(invoice.get("total_amount", 0)) for invoice in invoices)
        
        data.append(
            {
                "date": date,
                "no_of_orders": len(invoices),
                "total_amount": total_amount
            }
        )

    return columns, data

def get_columns():
    return [
        {"fieldname": "date", "label": "Date", "fieldtype": "Date", "width": 120},
        {"fieldname": "no_of_orders", "label": "Number of Orders", "fieldtype": "Int", "width": 150},
        {"fieldname": "total_amount", "label": "Total Amount", "fieldtype": "Float", "width": 150},
    ]

def generate_date_list(start_date, end_date):
    delta = end_date - start_date
    return [start_date + timedelta(days=i) for i in range(delta.days + 1)]