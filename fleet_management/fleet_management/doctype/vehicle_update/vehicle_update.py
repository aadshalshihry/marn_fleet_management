# Copyright (c) 2025, a Aalshehri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now


class VehicleUpdate(Document):
	def validate(self):
		"""Validate vehicle update data before saving"""
		# Auto-set driver from vehicle if not provided
		if self.vehicle and not self.driver:
			vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
			if vehicle_doc.current_driver:
				self.driver = vehicle_doc.current_driver

		# Update vehicle odometer if provided and greater than current
		if self.odometer_reading and self.vehicle:
			vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
			if not vehicle_doc.odometer_reading or self.odometer_reading > vehicle_doc.odometer_reading:
				vehicle_doc.odometer_reading = self.odometer_reading
				vehicle_doc.save()

	def on_submit(self):
		"""Process actions when update is submitted"""
		# Create maintenance request if required
		if self.maintenance_required:
			self.create_maintenance_request()

		# Update vehicle status if issues reported
		if self.issues_reported:
			self.update_vehicle_status()
		
		"""Create stock entry when vehicle update is submitted"""
		if self.maintenance_items:
			self.create_stock_entry()

	def create_maintenance_request(self):
		"""Create maintenance request if maintenance is required"""
		maintenance_doc = frappe.get_doc({
			"doctype": "Vehicle Maintenance",
			"vehicle": self.vehicle,
			"maintenance_type": "Preventive",
			"description": f"Maintenance required as reported in update {self.name}",
			"priority": "Medium",
			"status": "Scheduled",
			"requested_date": frappe.utils.today(),
			"reference_update": self.name
		})
		maintenance_doc.insert()
		frappe.msgprint(f"Maintenance request {maintenance_doc.name} created for vehicle {self.vehicle}")

	def update_vehicle_status(self):
		"""Update vehicle status based on reported issues"""
		vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
		if vehicle_doc.status == "Active":
			# Don't automatically change status, but notify fleet manager
			frappe.msgprint(f"Issues reported for vehicle {self.vehicle}. Please review and update status if needed.",
				alert=True)

	def create_stock_entry(self):
		"""Create Material Issue stock entry for maintenance items"""
		stock_entry = frappe.get_doc({
				"doctype": "Stock Entry",
				"stock_entry_type": "Material Issue",
				"purpose": "Material Issue",
				"company": self.company,
				"posting_date": self.date,
				"vehicle_update": self.name,  # Reference back
				"items": []
		})
		
		for item in self.maintenance_items:
			stock_entry.append("items", {
					"item_code": item.item_code,
					"qty": item.qty,
					"uom": item.uom,
					"s_warehouse": item.warehouse,  # Source warehouse
					"cost_center": self.cost_center if hasattr(self, 'cost_center') else None,
					"expense_account": self.get_expense_account(item.item_code)
			})
		
		stock_entry.insert()
		stock_entry.submit()
		
		frappe.msgprint(f"Stock Entry {stock_entry.name} created successfully")
		
		# Link stock entry to vehicle update
		self.db_set("stock_entry", stock_entry.name)

		def get_expense_account(self, item_code):
			"""Get expense account for the item"""
			item = frappe.get_doc("Item", item_code)
			return item.expense_account or frappe.get_cached_value(
					"Company", self.company, "default_expense_account"
			)

		def on_cancel(self):
			"""Cancel linked stock entry when vehicle update is cancelled"""
			if self.stock_entry:
				stock_entry = frappe.get_doc("Stock Entry", self.stock_entry)
				if stock_entry.docstatus == 1:
					stock_entry.cancel()
					frappe.msgprint(f"Stock Entry {self.stock_entry} cancelled")
