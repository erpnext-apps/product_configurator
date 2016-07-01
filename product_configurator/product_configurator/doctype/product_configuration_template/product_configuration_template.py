# -*- coding: utf-8 -*-
# Copyright (c) 2015, iXsystems, Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class ProductConfigurationTemplate(Document):
	pass

@frappe.whitelist()
def get_product_configuration_template(item_code):
	try:
		doc = frappe.get_doc("Product Configuration Template", {"item": item_code}).as_dict()
		for spec in doc.product_configuration_specs:
			if spec.item_group:
				# limit the search results to these sub items
				# this value is passed to the search function to limit the results
				spec.compatible_sub_items = [d[0] for d in
					frappe.db.sql("""select sub_item
						from `tabProduct Configuration Compatibility` as pcc
						where
							main_item = %s
							and exists (
								select name from `tabItem` as item
								where item.name=pcc.sub_item and item_group=%s
							)""", (item_code, spec.item_group))]

		return doc

	except frappe.DoesNotExistError:
		# we don't want to display "not found" to the user!
		frappe.message_log.pop()
		pass
