// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Invoice", {
    refresh: function (frm) {

    },
    order: function (frm) {
        console.log("hello")
        if (frm.doc.order) {
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Order",
                    filters: {
                        "name": frm.doc.order
                    },
                    fields: ["*"]
                },
                callback: function (response) {
                    if (response.message) {
                        order = response.message
                        frm.clear_table("invoice_items");

                        order.order_items.forEach(function (item) {
                            var child = frm.add_child("invoice_items");
                            frappe.model.set_value(child.doctype, child.name, "category", item.category);
                            frappe.model.set_value(child.doctype, child.name, "item", item.item);
                            frappe.model.set_value(child.doctype, child.name, "unit", item.unit);
                            frappe.model.set_value(child.doctype, child.name, "rate", item.rate);
                            frappe.model.set_value(child.doctype, child.name, "ordered_qty", item.ordered_qty);
                            frappe.model.set_value(child.doctype, child.name, "amount", item.amount);
                        });

                        frm.refresh_field("invoice_items");
                    }
                }
            });
        }
    }
});

frappe.ui.form.on("Invoice Items", {
    order_items_add: function (frm, cdt, cdn) {
        calc_total_amount(frm)
    },

    order_items_remove: function (frm, cdt, cdn) {
        calc_total_amount(frm)
    },

    ordered_qty: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];

        row.amount = row.rate * row.ordered_qty;
        frm.refresh_field('invoice_items');
        calc_total_amount(frm)
    }
});

function calc_total_amount(frm) {
    let total_amount = 0

    frm.doc.invoice_items.forEach(function (row) {
        total_amount += row.amount
    });

    frm.set_value("total_amount", total_amount)
}