# Copyright (c) 2025, a Aalshehri and Contributors
# See license.txt

import frappe
import unittest


class TestDriver(unittest.TestCase):
	def test_driver_creation(self):
		"""Test basic driver creation"""
		driver = frappe.get_doc({
			"doctype": "Driver",
			"naming_series": "DRV-.YYYY.-",
			"driver_name": "John Doe",
			"phone": "+1234567890",
			"license_number": "DL123456789",
			"status": "Active"
		})
		driver.insert()
		self.assertEqual(driver.driver_name, "John Doe")
		driver.delete()

	def test_phone_validation(self):
		"""Test phone number validation"""
		driver = frappe.get_doc({
			"doctype": "Driver",
			"naming_series": "DRV-.YYYY.-",
			"driver_name": "Jane Doe",
			"phone": "invalid-phone",
			"license_number": "DL987654321",
			"status": "Active"
		})
		with self.assertRaises(frappe.ValidationError):
			driver.insert()
