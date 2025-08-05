# Copyright (c) 2025, a Aalshehri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate


class VehicleMaintenance(Document):
	def validate(self):
		"""Validate maintenance data before saving"""
		# Set completion date if status is completed
		if self.status == "Completed" and not self.completed_date:
			self.completed_date = today()

		# Update vehicle odometer if provided
		if self.odometer_reading and self.vehicle:
			vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)
			if not vehicle_doc.odometer_reading or self.odometer_reading > vehicle_doc.odometer_reading:
				vehicle_doc.odometer_reading = self.odometer_reading
				vehicle_doc.save()

	def on_update(self):
		"""Update related records when maintenance is updated"""
		if self.has_value_changed("status"):
			self.update_vehicle_status()

	def update_vehicle_status(self):
		"""Update vehicle status based on maintenance status"""
		vehicle_doc = frappe.get_doc("Vehicle", self.vehicle)

		if self.status == "In Progress" and self.priority in ["High", "Critical"]:
			if vehicle_doc.status == "Active":
				vehicle_doc.status = "Maintenance"
				vehicle_doc.save()
				frappe.msgprint(f"Vehicle {vehicle_doc.vehicle_name} status updated to Maintenance")

		elif self.status == "Completed":
			if vehicle_doc.status == "Maintenance":
				vehicle_doc.status = "Active"
				vehicle_doc.save()
				frappe.msgprint(f"Vehicle {vehicle_doc.vehicle_name} status updated to Active")

	def get_total_cost(self):
		"""Calculate total cost including parts"""
		total = self.actual_cost or 0
		for part in self.parts_used:
			if part.cost:
				total += part.cost
		return total
