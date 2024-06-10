// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Invoice Items", {
    item: function (frm, cdt, cdn) {
        let row = locals[cdt][cdn];
        if (row.item) {
            frappe.db.get_doc('Item', row.item)
                .then(item => {
                    frappe.model.set_value(cdt, cdn, 'ordered_qty', item.min_qty);
                });
        }
    }, 
    ordered_qty: function (frm, cdt, cdn) {
        var row = locals[cdt][cdn];

        row.amount = row.rate * row.ordered_qty;
        frm.refresh_field('invoice_items');
        total_amount(frm)
    }
});

function total_amount(frm) {
    let total_amount = 0

    frm.doc.order_items.forEach(function (row) {
        total_amount += row.amount
    });

    frm.set_value("total_amount", total_amount)
}