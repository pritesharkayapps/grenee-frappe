// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.query_reports["Invoice Report"] = {
	"filters": [
        {
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            // "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30)
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            // "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "user",
            "label": "Franchise Name",
            "fieldtype": "Link",
            "options": "User"
        }
    ]
};
