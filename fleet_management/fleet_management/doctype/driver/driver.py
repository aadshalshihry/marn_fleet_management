# Copyright (c) 2025, a Aalshehri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today, getdate


class Driver(Document):
	def validate(self):
		"""Validate driver data before saving"""
		# Check license expiry
		if self.license_expiry and getdate(self.license_expiry) < getdate(today()):
			frappe.msgprint(f"Driver license for {self.driver_name} has expired!", alert=True)

		# Validate phone number format
		if self.phone and not self.phone.replace('+', '').replace('-', '').replace(' ', '').isdigit():
			frappe.throw("Please enter a valid phone number")

	def on_update(self):
		"""Update related records when driver is updated"""
		if self.has_value_changed("status") and self.status == "Inactive":
			self.unassign_vehicles()

	def unassign_vehicles(self):
		"""Unassign vehicles when driver becomes inactive"""
		vehicles = frappe.get_all("Vehicle",
			filters={"current_driver": self.name},
			fields=["name"])

		for vehicle in vehicles:
			vehicle_doc = frappe.get_doc("Vehicle", vehicle.name)
			vehicle_doc.current_driver = None
			vehicle_doc.assigned_date = None
			vehicle_doc.save()
			frappe.msgprint(f"Vehicle {vehicle_doc.vehicle_name} has been unassigned from {self.driver_name}")

	def get_assigned_vehicles(self):
		"""Get list of vehicles assigned to this driver"""
		return frappe.get_all("Vehicle",
			filters={"current_driver": self.name, "status": "Active"},
			fields=["name", "vehicle_name", "license_plate", "make", "model"])
