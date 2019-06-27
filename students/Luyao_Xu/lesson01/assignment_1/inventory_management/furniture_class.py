"""
This module contains definitions of Furniture.
"""
from .inventory_class import Inventory


class Furniture(Inventory):
    """
    Defines a Furniture
    """

    def __init__(self, product_code, description, market_price, rental_price,
                 material, size):
        """
        Initialize the class
        :param product_code:
        :param description:
        :param market_price:
        :param rental_price:
        :param material:
        :param size:
        """
        # Creates common instance variables from the parent class
        Inventory.__init__(self, product_code, description, market_price,
                           rental_price)

        self.material = material
        self.size = size

    def return_as_dictionary(self):
        """
        Return class's metadata
        :return:
        """
        output_dict = Inventory.return_as_dictionary(self)
        output_dict['material'] = self.material
        output_dict['size'] = self.size

        return output_dict