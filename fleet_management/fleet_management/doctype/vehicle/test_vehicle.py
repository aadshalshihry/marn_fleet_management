# Copyright (c) 2025, a Aalshehri and Contributors
# See license.txt

import frappe
import unittest


class TestVehicle(unittest.TestCase):
	def test_vehicle_creation(self):
		"""Test basic vehicle creation"""
		vehicle = frappe.get_doc({
			"doctype": "Vehicle",
			"naming_series": "VEH-.YYYY.-",
			"vehicle_name": "Test Vehicle",
			"license_plate": "ABC123",
			"make": "Toyota",
			"model": "Camry",
			"year": 2020,
			"vehicle_type": "Car",
			"fuel_type": "Petrol",
			"status": "Active"
		})
		vehicle.insert()
		self.assertEqual(vehicle.license_plate, "ABC123")
		vehicle.delete()

	def test_license_plate_uppercase(self):
		"""Test that license plate is converted to uppercase"""
		vehicle = frappe.get_doc({
			"doctype": "Vehicle",
			"naming_series": "VEH-.YYYY.-",
			"vehicle_name": "Test Vehicle 2",
			"license_plate": "xyz789",
			"make": "Honda",
			"model": "Civic",
			"vehicle_type": "Car",
			"status": "Active"
		})
		vehicle.insert()
		self.assertEqual(vehicle.license_plate, "XYZ789")
		vehicle.delete()
