# -*- coding: utf-8 -*-
from __future__ import unicode_literals

app_name = "product_configurator"
app_title = "Product Configurator"
app_publisher = "iXsystems, Inc."
app_description = "Product Configurator"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "matt@ixsystems.com"
app_version = "0.0.1"

hide_in_installer = True

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/product_configurator/css/product_configurator.css"
# app_include_js = "/assets/product_configurator/js/product_configurator.js"

# include js, css files in header of web template
# web_include_css = "/assets/product_configurator/css/product_configurator.css"
# web_include_js = "/assets/product_configurator/js/product_configurator.js"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

fixtures = ['Custom Field', 'Print Format']
doctype_js = {
        "Quotation": "product_configurator/quotation.js"
        }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "product_configurator.install.before_install"
# after_install = "product_configurator.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "product_configurator.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }
doc_event = {
    "Quotation": {
        "validate": "product_configurator.product_configurator.quotation.validate_product_configuration_compatibility"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"product_configurator.tasks.all"
# 	],
# 	"daily": [
# 		"product_configurator.tasks.daily"
# 	],
# 	"hourly": [
# 		"product_configurator.tasks.hourly"
# 	],
# 	"weekly": [
# 		"product_configurator.tasks.weekly"
# 	]
# 	"monthly": [
# 		"product_configurator.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "product_configurator.install.before_tests"

# Overriding Whitelisted Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "product_configurator.event.get_events"
# }

