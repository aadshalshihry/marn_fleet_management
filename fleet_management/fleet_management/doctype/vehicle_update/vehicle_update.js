// Copyright (c) 2025, Aalshehri and contributors
// For license information, please see license.txt

frappe.ui.form.on("Vehicle Update", {
	refresh(frm) {

	},
  update_type: function(frm) {
    if (frm.doc.update_type === "Maintenance") {
      frm.toggle_display('stock_section', frm.doc.update_type);
    }
  }
});

frappe.ui.form.on('Vehicle Maintenance Item', {
  qty: function (frm, cdt, cdn) {
    calculate_amount(frm, cdt, cdn);
  },
  rate: function (frm, cdt, cdn) {
    calculate_amount(frm, cdt, cdn);
  }
});

function calculate_amount(frm, cdt, cdn) {
  let row = locals[cdt][cdn];
  row.amount = flt(row.qty) * flt(row.rate);
  frm.refresh_field('maintenance_items');
}

frappe.ui.form.on('Vehicle Update', {
  refresh: function (frm) {
    if (frm.doc.stock_entry) {
      frm.add_custom_button(__('View Stock Entry'), function () {
        frappe.set_route('Form', 'Stock Entry', frm.doc.stock_entry);
      });
    }
  }
});