# Copyright (c) 2025, a Aalshehri and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Vehicle(Document):
	def validate(self):
		"""Validate vehicle data before saving"""
		# Ensure license plate is uppercase
		if self.license_plate:
			self.license_plate = self.license_plate.upper()

		# Validate year
		if self.year and (self.year < 1900 or self.year > frappe.utils.nowdate().year + 1):
			frappe.throw(f"Invalid year: {self.year}")

	def on_update(self):
		"""Update related records when vehicle is updated"""
		# Update driver assignment if changed
		if self.has_value_changed("current_driver"):
			self.update_driver_assignment()

	def update_driver_assignment(self):
		"""Update driver assignment history"""
		if self.current_driver:
			# Create assignment record or update existing
			pass
