frappe.ui.form.on("Product Configuration Template", {
	onload: function(frm) {
		frm.set_query('default_item', 'product_configuration_specs', function(doc, cdt, cdn) {
			var spec = frappe.model.get_doc(cdt, cdn);
			return {
				'query': 'product_configurator.utils.query_configuration_item',
				'filters': {
					'item': frm.doc.item,
					'item_group': spec.item_group
				}
			}
		});
	}
});

