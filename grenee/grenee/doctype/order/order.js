// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on('Order', {
    refresh(frm) {
        if (frm.doc.workflow_state == "Confirmed" || frm.doc.workflow_state == "Closed") {
            frm.add_custom_button(__('Generate Invoice'), function () {
                frappe.route_options = {
                    "order": frm.doc.name
                };
                frappe.new_doc('Invoice');
            });
        }
    }
})

frappe.ui.form.on("Order Items", {
    order_items_add: function(frm, cdt, cdn) {
        calc_total_amount(frm)
    },

    order_items_remove: function(frm, cdt, cdn) {
        calc_total_amount(frm)
    },

    ordered_qty: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];

        if (row.ordered_qty % row.lot_qty != 0) {
            add_qty = row.ordered_qty % row.lot_qty
            row.ordered_qty += row.lot_qty - add_qty
        }

        row.amount = row.rate * row.ordered_qty;
        frm.refresh_field('order_items');
        calc_total_amount(frm)
    }
});

function calc_total_amount(frm) {
    let total_amount = 0

    frm.doc.order_items.forEach(function (row) {
        total_amount += row.amount
    });

    frm.set_value("total_amount", total_amount)
}