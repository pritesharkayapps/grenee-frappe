// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on('Order', {
    refresh(frm) {
        if (frm.doc.workflow_state == "Confirmed" || frm.doc.workflow_state == "Closed") {
            frm.add_custom_button(__('Generate Invoice'), function () {
                frappe.call({
                    method: 'frappe.client.insert',
                    args: {
                        doc: {
                            doctype: 'Invoice',
                            order: frm.doc.name,
                            user: frm.doc.user,
                            invoice_date_time: frappe.datetime.now_datetime(),
                            invoice_items: frm.doc.order_items.map(item => ({
                                category: item.category,
                                item: item.item,
                                unit: item.unit,
                                rate: item.rate,
                                ordered_qty: item.ordered_qty,
                                amount: item.amount
                            })),
                            total_amount: frm.doc.total_amount
                        }
                    },
                    callback: function (response) {
                        if (response.message) {
                            frappe.set_route('Form', 'Invoice', response.message.name);
                        }
                    }
                });
            });
        }
    }
})

frappe.ui.form.on("Order Items", {
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

        if (row.ordered_qty % row.lot_qty != 0) {
            add_qty = row.ordered_qty % row.lot_qty
            row.ordered_qty += row.lot_qty - add_qty
        }

        row.amount = row.rate * row.ordered_qty;
        frm.refresh_field('order_items');
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