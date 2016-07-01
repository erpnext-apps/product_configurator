# -*- coding: utf-8 -*-
# Copyright (c) 2015, iXsystems, Inc. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from erpnext.controllers.queries import item_query

def query_configuration_item(doctype, txt, searchfield, start, page_len, filters):
	main_item = filters['item']
	sub_items = [d.sub_item for d in frappe.get_all('Product Configuration Compatibility',
		filters={ 'main_item': main_item }, fields=['sub_item'])]
	item_filters = [['Item', 'item_code', 'in', sub_items]]

	if filters.get('item_group'):
		item_filters.append(['Item', 'item_group', '=', filters['item_group']])

	return item_query('Item', txt, 'name', start, page_len, item_filters)
