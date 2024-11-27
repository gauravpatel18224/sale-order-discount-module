from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    discount_amount = fields.Float(string="Discount Amount", compute="_compute_discount_details", store=True)
    discount_percentage = fields.Float(string="Discount Percentage", compute="_compute_discount_details", store=True)

    @api.depends('order_line.price_unit', 'order_line.product_uom_qty', 'order_line.discount', 'amount_untaxed')
    def _compute_discount_details(self):
        for order in self:
            total_discount = 0.0  # Initialize total discount
            total_original_amount = 0.0  # Initialize total original amount

            # Loop through each order line to calculate the discount for each line
            for line in order.order_line:
                # Calculate the discount for each line: (price * quantity) * discount percentage
                line_discount = (line.price_unit * line.product_uom_qty * line.discount) / 100
                total_discount += line_discount  # Add the line discount to total discount
                total_original_amount += line.price_unit * line.product_uom_qty  # Add the original price to the total amount

            # Set the total discount amount for the order
            order.discount_amount = total_discount

            # Calculate the total discount percentage
            order.discount_percentage = (total_discount / total_original_amount * 100) if total_original_amount > 0 else 0.0
