# Copyright (c) 2025, a Aalshehri and Contributors
# See license.txt

import frappe
import unittest


class TestVehicleUpdate(unittest.TestCase):
	def setUp(self):
		# Create test data
		self.test_vehicle = frappe.get_doc({
			"doctype": "Vehicle",
			"naming_series": "VEH-.YYYY.-",
			"vehicle_name": "Test Vehicle",
			"license_plate": "TEST123",
			"make": "Toyota",
			"model": "Camry",
			"vehicle_type": "Car",
			"status": "Active"
		}).insert()

		self.test_driver = frappe.get_doc({
			"doctype": "Driver",
			"naming_series": "DRV-.YYYY.-",
			"driver_name": "Test Driver",
			"phone": "+1234567890",
			"license_number": "TEST123456",
			"status": "Active"
		}).insert()

	def tearDown(self):
		# Clean up test data
		self.test_vehicle.delete()
		self.test_driver.delete()

	def test_vehicle_update_creation(self):
		"""Test basic vehicle update creation"""
		update = frappe.get_doc({
			"doctype": "Vehicle Update",
			"naming_series": "VUP-.YYYY.-",
			"vehicle": self.test_vehicle.name,
			"driver": self.test_driver.name,
			"update_type": "Daily Check",
			"description": "Daily vehicle inspection completed"
		})
		update.insert()
		self.assertEqual(update.vehicle, self.test_vehicle.name)
		update.delete()
