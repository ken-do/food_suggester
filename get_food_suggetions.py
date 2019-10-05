import sys, csv, pandas
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def make_suggestion(inFileName, outFileName):
    input = read_input(inFileName)
    write_suggestions(get_suggestions(input), outFileName)


def read_input(inFileName):
    with open(inFileName, 'r') as infile:
        csv_reader = csv.reader(infile.read().splitlines())
        return next(csv_reader)


def write_suggestions(suggestions, outFileName):
    print(suggestions)
    with open(outFileName, 'w') as outfile:
        for suggestion in suggestions:
            csv_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(suggestion)


def get_suggestions(input):
    
    input_ingredients = np.array([input])

    url = "./data.csv"
    dataset = pandas.read_csv(url)
    datashape = dataset.shape
    array = dataset.values
    
    ingredient_names = dataset.columns.values[:datashape[1] - 1]
    food_names = array[1:,datashape[1] - 1]
    based_instances = array[1:,0:datashape[1] - 1]

    return find_suggestions(based_instances, food_names, input_ingredients)


def find_suggestions(based_instances, food_names, input_ingredients):
    suggestions = {}
    for index, item in enumerate(based_instances):
        
        food = food_names[index]
        validation_item = item.reshape(1, -1)

        has_not_allowed = check_not_allowed(validation_item, input_ingredients)

        if(has_not_allowed):
            continue
        else:
            suggestions[food] = cosine_similarity(input_ingredients, validation_item)[0][0]
    
    return sorted(suggestions.items(), key=lambda x: x[1], reverse=True)


def check_not_allowed(validation_item, input_ingredients):
    for index, attribute in enumerate(input_ingredients[0]):
        if(int(attribute) == 0 and int(validation_item[0][index]) == 1):
            return True
    return False


if __name__ == "__main__":
    if( len(sys.argv) > 2 ):
        make_suggestion(sys.argv[1], sys.argv[2])
    else:
        print('Please provide a command line using this format: python get_food_suggestions.py [input_file.csv] [out_file.csv]')