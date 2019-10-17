# Furniture class

"""
Furniture Moduel

Classes:
    Furniture
"""

from inventory_class import Inventory


class Furniture(Inventory):
    """ An object representing an item of Furnature """

    def __init__(self, product_code, description, market_price, rental_price, material, size):
        """
        Initializes the Furnature class object.

        :self:          The Class
        :product_code:  The product code of the furnature
        :description:   The furnature description
        :market_price:  The market cost of the furnature
        :rental_price:  The rental price of the furnature
        :material:      The material the furnature is made of
        """
        Inventory.__init__(self, product_code, description, market_price, rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        Return a dictionary representing the Furnature object
        """
        output_dict = {}
        output_dict['product_code'] = self.product_code
        output_dict['description'] = self.description
        output_dict['market_price'] = self.market_price
        output_dict['rental_price'] = self.rental_price
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict
