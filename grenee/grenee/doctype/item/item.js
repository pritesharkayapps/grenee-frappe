// Copyright (c) 2024, Pritesh Kerai and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item", {
    item_code: function (frm) {
        const item_code = frm.doc.item_code;
        if (item_code) {
            frm.set_value('item_name', item_code);
        }
    }
});
