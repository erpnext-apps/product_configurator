frappe.ui.form.on("Quotation Item", {
	"configure": function(frm, doctype, docname) {
		var item = frappe.get_doc(doctype, docname);
		frm.fields_dict.items.grid.open_grid_row.hide_form();
		product_configurator.get_configuration_template(frm, item);
	},
	"clear_configuration": function(frm, doctype, docname) {
		var item = frappe.get_doc(doctype, docname);
		var configs = product_configurator.get_product_configuration_for_item(frm, item);
		$.each(configs, function(i, config) {
			frappe.model.clear_doc(config.doctype, config.name);
		});
		frm.refresh_field("product_configuration");
	}
});

frappe.provide("product_configurator");
product_configurator.get_product_configuration_for_item = function(frm, item) {
	return frappe.model.get_list("Product Configuration", {
		"parent": frm.doc.name,
		"main_item": item.item_code
	});
}

product_configurator.get_configuration_template = function(frm, item) {
	// check if product configuration already exists for this item
	var product_configuration = product_configurator.get_product_configuration_for_item(frm, item);
	if (!product_configuration.length) {
		// not found! get the product configuration template for the item if it exists
		frappe.call({
			method: "product_configurator.product_configurator.doctype.product_configuration_template.product_configuration_template.get_product_configuration_template",
			args: {
				"item_code": item.item_code
			},
			callback: function(r) {
				// if not found, do nothing
				if (!r.message) {
					return;
				}
				product_configurator.open_configurator_dialog(frm, item, r);
			}
		});
	}
};

product_configurator.open_configurator_dialog = function(frm, item, r) {
	var product_configuration_template = r.message;
	var product_configuration_specs = product_configuration_template.product_configuration_specs;
	var fields_list = [];
	
	// build a list of fields to be rendered in the dialog box
	$.each(product_configuration_specs, function(i, spec) {
		var fieldname = spec.label.toLowerCase().replace(" ", "_");
		spec.fieldname = fieldname;
		
		if (spec.item_group) {
			// if it is supposed to be an item selector, render item link field with item group filter and quantity field
			fields_list.push({
				fieldname: fieldname,
				label: spec.label,
				fieldtype: "Link",
				options: "Item",
				default: spec.default_item,
				get_query: function() {
					return {
						"filters": [
							// we get the list of compatible sub items from the get_configuration_template function
							// these filters will limit the list of items to only compatible items of this item group
							["Item", "name", "in", spec.compatible_sub_items],
							["Item", "item_group", "=", spec.item_group]
						]
					};
				}
			});
			// column break is added for good looks
			fields_list.push({
				fieldtype: "Column Break"
			});
			fields_list.push({
				fieldname: fieldname + "_quantity",
				label: "Quantity",
				fieldtype: "Int",
				default: spec.default_quantity
			});
		} else {
			// if it is supposed to be just a description, render a text editor field with label
			// TODO make it readonly
			fields_list.push({
				fieldname: fieldname,
				label: spec.label,
				fieldtype: "Text Editor",
				default: spec.description,
				read_only: 1
			});
		}
		
		// a section break is added for looks
		fields_list.push({
			fieldtype: "Section Break"
		})
	});

	var dialog = new frappe.ui.Dialog({
		fields: fields_list,
		title: __("Configure {0}", [product_configuration_template.item]),
		primary_action_label: __("Okay"),
		primary_action: function() {
			product_configurator.process_product_configuration(frm, item, dialog, product_configuration_specs);
		}
	});
	dialog.show();
};

product_configurator.process_product_configuration = function(frm, item, dialog, product_configuration_specs) {
	// once configured, send the whole doc and the selected configuration to server for post processing like adding item's description, validation of compatibility and quantity, and deciding the price of the main item
	var out = [];
	for (var i=0, l=product_configuration_specs.length; i < l; i++) {
		var spec = product_configuration_specs[i];
		out.push({
			label: spec.label,
			is_description: spec.item_group ? 0 : 1,
			value: dialog.get_value(spec.fieldname),
			sub_quantity: spec.item_group ? dialog.get_value(spec.fieldname + "_quantity") : null
		});
	}
	frappe.call({
		method: "product_configurator.product_configurator.quotation.process_product_configuration",
		args: {
			doc: frm.doc,
			main_item: item.item_code,
			product_configuration: out
		},
		callback: function(r) {
			dialog.hide();
			frappe.model.sync(r.message);
			frm.refresh();
		}
	})
};
