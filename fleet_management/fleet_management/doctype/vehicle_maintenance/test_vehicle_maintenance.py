# Copyright (c) 2025, a Aalshehri and Contributors
# See license.txt

import frappe
import unittest


class TestVehicleMaintenance(unittest.TestCase):
	def setUp(self):
		# Create test vehicle
		self.test_vehicle = frappe.get_doc({
			"doctype": "Vehicle",
			"naming_series": "VEH-.YYYY.-",
			"vehicle_name": "Test Vehicle",
			"license_plate": "MAINT123",
			"make": "Toyota",
			"model": "Camry",
			"vehicle_type": "Car",
			"status": "Active"
		}).insert()

	def tearDown(self):
		# Clean up test data
		self.test_vehicle.delete()

	def test_maintenance_creation(self):
		"""Test basic maintenance creation"""
		maintenance = frappe.get_doc({
			"doctype": "Vehicle Maintenance",
			"naming_series": "VM-.YYYY.-",
			"vehicle": self.test_vehicle.name,
			"maintenance_type": "Preventive",
			"description": "Regular service",
			"priority": "Medium",
			"status": "Scheduled"
		})
		maintenance.insert()
		self.assertEqual(maintenance.vehicle, self.test_vehicle.name)
		maintenance.delete()
