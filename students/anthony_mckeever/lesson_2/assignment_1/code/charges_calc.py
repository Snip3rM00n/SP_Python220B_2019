'''
Returns total price paid for individual rentals 
'''
import argparse
import datetime
import json
import logging
import math

from argparse import RawTextHelpFormatter

def parse_cmd_arguments():
    debug_help = str('Sets the logging level.' +
                     '\nAccepted values:'
                     '\n\t0 - None (default)' +
                     '\n\t1 - errors only' +
                     '\n\t2 - errors and warnings,' +
                     '\n\t3 - errors, warnings and debug messages')
    
    parser = argparse.ArgumentParser(description='Process some integers.',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-i', '--input',
                        help='input JSON file', required=True)
    parser.add_argument('-o', '--output',
                        help='ouput JSON file', required=True)
    parser.add_argument('-d', '--debug', type=int, default=0, help=debug_help)

    return parser.parse_args()

def set_logging(level):
    log_level = parse_log_level(level)
    logging.basicConfig()
    logging.info("Log level set to ")

def parse_log_level(level):
    if level == 0:
        return logging.NOTSET
    elif level == 1:
        return logging.ERROR
    elif level == 2:
        return logging.WARNING
    elif level == 3:
        return logging.CRITICAL

def load_rentals_file(filename):
    with open(filename) as file:
        try:
            data = json.load(file)
        except:
            exit(0)
    return data

def calculate_additional_fields(data):
    for value in data.values():
        try:
            rental_start = datetime.datetime.strptime(value['rental_start'], '%m/%d/%y')
            rental_end = datetime.datetime.strptime(value['rental_end'], '%m/%d/%y')
            value['total_days'] = (rental_end - rental_start).days
            value['total_price'] = value['total_days'] * value['price_per_day']
            value['sqrt_total_price'] = math.sqrt(value['total_price'])
            value['unit_cost'] = value['total_price'] / value['units_rented']
        except Exception as e:
            print(e)
            exit(0)

    return data

def save_to_json(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file)

if __name__ == "__main__":
    args = parse_cmd_arguments()
    
    data = load_rentals_file(args.input)
    data = calculate_additional_fields(data)
    save_to_json(args.output, data)
