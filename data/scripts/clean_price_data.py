import csv
import sys


# Custom exception for debugging
class ArgException(Exception):
    pass

# Make sure the right number of arguments got passed in
try:
    assert sys.argv[1]
    assert sys.argv[2]
except IndexError as e:
    raise ArgException("The script clean_price_data.py requires two " +
                       "arguments: `filename` and `year`. Check to see " +
                       "that you included both.")

# Global vars
FILENAME = sys.argv[1].split('/')[2]
YEAR = sys.argv[2]
PREV_YEAR = str(int(YEAR)-1)
CHANGE = 'change'
SUFFIXES = [PREV_YEAR, YEAR, CHANGE]

# Read in the CSV
reader = csv.reader(sys.stdin)
in_header = next(reader)

# Chicago data
if len(in_header) <= 8:

    # Map input rows to output columns
    variables = [
        'new_listings',
        'closed_sales',
        'median_price',
        'percent_of_list_price_received',
        'market_time',
        'inventory_for_sale'
    ]
    var_labels = [
        'New Listings',
        'Closed Sales',
        'Median Sales Price*',
        'Percent of Original List Price Received*',
        'Market Time',
        'Inventory of Homes for Sale'
    ]
    var_map = {label: var for (label, var) in zip(var_labels, variables)}

    # Bring the CSV into memory so we can split the tables
    data = [row for row in reader]
    detached = data[:8]
    attached = data[8:]

    attached_results = {}
    for row in attached:
        try:
            # Check if first col is empty
            if row[0] == '':
                attached_results[var_map[row[1]]] = row[5:]
            else:
                attached_results[var_map[row[0]]] = row[4:]

        except KeyError:
            # If the row value doesn't match a variable, skip it
            continue

    detached_results = {}
    for row in detached:
        try:
            if row[0] == '':
                detached_results[var_map[row[1]]] = row[5:]
            else:
                detached_results[var_map[row[0]]] = row[4:]
        except KeyError:
            continue

    # Build a dict of values to store the results
    output = {}
    for key in attached_results:
        for label, val in zip(SUFFIXES, attached_results[key]):
            output['_'.join(('attached', key, label))] = val

    for key in detached_results:
        for label, val in zip(SUFFIXES, detached_results[key]):
            output['_'.join(('detached', key, label))] = val

    # Build a header row
    prefixes = ['detached', 'attached']
    zipped = [[pre, var, suf] for pre in prefixes for var in variables for suf in SUFFIXES]
    fieldnames = ['community'] + ['_'.join(name) for name in zipped]

    # Figure out the name of this community and add it to the dict of values
    if '.pdf' in FILENAME:
        place = FILENAME.split('.pdf')[0].replace('_', ' ').upper()
    else:
        # For debugging
        assert '.csv' in FILENAME
        place = FILENAME.split('.csv')[0].replace('_', ' ').upper()
    output['community'] = place

    # Write the output
    writer = csv.DictWriter(sys.stdout,
                            fieldnames=fieldnames,
                            quoting=csv.QUOTE_MINIMAL)
    writer.writeheader()
    writer.writerow(output)

# # Handle suburbs
# else:
#     location = 'suburbs'
