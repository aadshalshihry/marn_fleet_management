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
