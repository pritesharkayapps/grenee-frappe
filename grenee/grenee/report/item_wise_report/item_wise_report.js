// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.query_reports["Item Wise Report"] = {
	"filters": [
		{
            "fieldname": "from_date",
            "label": "From Date",
            "fieldtype": "Date",
            // "default": frappe.utils.add_days(frappe.utils.today(), -30),
            // "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": "To Date",
            "fieldtype": "Date",
            // "default": frappe.utils.today(),
            // "reqd": 1
        }
	]
};
