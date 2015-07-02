# -*- coding: utf-8 -*-
# Copyright (c) 2015, iXsystems, Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import json
from frappe.utils import flt

@frappe.whitelist()
def process_product_configuration(doc, main_item, product_configuration):
	product_configuration = json.loads(product_configuration)
	doc = frappe.get_doc(json.loads(doc))
	
	append_product_configuration(doc, main_item, product_configuration)

	main_item_doc = doc.get("items", {"item_code": main_item})[0]
	main_item_doc.price_list_rate = add_rates_of_sub_items(doc, main_item_doc)
	
	# before sending back the doc to the client, calculate totals
	validate_product_configuration_compatibility(doc)
	doc.calculate_taxes_and_totals()
	
	return doc
	
def append_product_configuration(doc, main_item, product_configuration):
	for configuration in product_configuration:
		configuration = frappe._dict(configuration);
		
		# decide what should be the description
		# if it is an item, get description from the item document
		if not configuration.is_description:
			configuration.description = frappe.db.get_value("Item", configuration.value, "description")
		else:
			configuration.description = configuration.value
		
		item = None
		if not configuration.is_description:
			item = configuration.value
			
		doc.append("product_configuration", {
			"label": configuration.label,
			 "description": configuration.description,
			 "main_item": main_item,
			 "item": item,
			 "sub_quantity": configuration.sub_quantity
		})

def add_rates_of_sub_items(doc, main_item_doc):
	item_rate = 0.0
	
	for config in doc.product_configuration:
		if config.item and config.main_item==main_item_doc.item_code:
			
			# get item price for the sub item using the price list specified in the doc
			sub_item_rate = frappe.db.get_value("Item Price", 
				{ "price_list": doc.selling_price_list, "item_code": config.item }, 
				"price_list_rate")
			
			if sub_item_rate:
				# sub item rate is multipled by exchange rate for price list and sub quantity
				item_rate += flt(sub_item_rate * doc.plc_conversion_rate * config.sub_quantity,
					main_item_doc.precision("price_list_rate"))
	
	return item_rate
	
def validate_product_configuration_compatibility(doc, method=None):
	if not doc.product_configuration:
		return

	for config in doc.product_configuration:
		if config.item:
			compatibility = frappe.db.get_value("Product Configuration Compatibility", 
				{ "main_item": config.main_item, "sub_item": config.item },
				["name", "max_quantity"], as_dict=True)
				
			if not compatibility:
				frappe.throw(_("Sub Product: {0} is not compatible with Main Product: {1}").format(config.item, config.main_item))
				
			if compatibility.max_quantity and config.sub_quantity > compatibility.max_quantity:
				uom = frappe.db.get_value("Item", config.item, "stock_uom")
				frappe.throw(_("Sub Product: {0} cannot have more than {1} {2}").format(config.item, compatibility.max_quantity, uom))
			
