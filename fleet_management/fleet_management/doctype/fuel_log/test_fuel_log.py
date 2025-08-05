# Copyright (c) 2025, a Aalshehri and Contributors
# See license.txt

import frappe
import unittest


class TestFuelLog(unittest.TestCase):
	def setUp(self):
		# Create test data
		self.test_vehicle = frappe.get_doc({
			"doctype": "Vehicle",
			"naming_series": "VEH-.YYYY.-",
			"vehicle_name": "Test Vehicle",
			"license_plate": "FUEL123",
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
			"license_number": "FUEL123456",
			"status": "Active"
		}).insert()

	def tearDown(self):
		# Clean up test data
		self.test_vehicle.delete()
		self.test_driver.delete()

	def test_fuel_log_creation(self):
		"""Test basic fuel log creation"""
		fuel_log = frappe.get_doc({
			"doctype": "Fuel Log",
			"naming_series": "FL-.YYYY.-",
			"vehicle": self.test_vehicle.name,
			"driver": self.test_driver.name,
			"odometer_reading": 10000,
			"fuel_type": "Petrol",
			"quantity": 50,
			"total_cost": 200
		})
		fuel_log.insert()
		self.assertEqual(fuel_log.vehicle, self.test_vehicle.name)
		fuel_log.delete()
