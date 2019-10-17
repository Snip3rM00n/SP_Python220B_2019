# Launches the user interface for the inventory management system
import sys

import market_prices
from inventory_class import Inventory
from furniture_class import Furniture
from electric_appliances_class import ElectricAppliances

def mainMenu(user_prompt=None):
    valid_prompts = {"1": addNewItem,
                     "2": itemInfo,
                     "q": exitProgram}
    options = list(valid_prompts.keys())

    while user_prompt not in valid_prompts:
        options_str = ("{}" + (", {}") * (len(options)-1)).format(*options)
        print("Please choose from the following options ({options_str}):")
        print("1. Add a new item to the inventory")
        print("2. Get item information")
        print("q. Quit")
        user_prompt = input(">")
    return valid_prompts.get(user_prompt)

def getPrice(item_code):
    print("Get price")

def addNewItem():
    global fullInventory
    item_code = input("Enter item code: ")
    item_description = input("Enter item description: ")
    item_rental_price = input("Enter item rental price: ")

    # Get price from the market prices module
    item_price = market_prices.get_latest_price(item_code)

    is_furniture = input("Is this item a piece of furniture? (Y/N): ")
    if is_furniture.lower() == "y":
        item_material = input("Enter item material: ")
        item_size = input("Enter item size (S,M,L,XL): ")
        new_item = Furniture(item_code,
                             item_description,
                             item_price,
                             item_rental_price,
                             item_material,
                             item_size)
    else:
        is_electric_appliance = input("Is this item an electric appliance? (Y/N): ")
        if is_electric_appliance.lower() == "y":
            item_brand = input("Enter item brand: ")
            item_voltage = input("Enter item voltage: ")
            new_item = ElectricAppliances(item_code,
                                          item_description,
                                          item_price,
                                          item_rental_price,
                                          item_brand,
                                          item_voltage)
        else:
            new_item = Inventory(item_code, item_description, item_price, item_rental_price)
    fullInventory[item_code] = new_item.return_as_dictionary()
    print("New inventory item added")


def itemInfo():
    item_code = input("Enter item code: ")

    if item_code in fullInventory:
        print_dict = fullInventory[item_code]

        for key, value in print_dict.items():
            print("{}:{}".format(key, value))

    else:
        print("Item not found in inventory")

def exitProgram():
    sys.exit()

if __name__ == '__main__':
    fullInventory = {}
    while True:
        print(fullInventory)
        mainMenu()()
        input("Press Enter to continue...........")
