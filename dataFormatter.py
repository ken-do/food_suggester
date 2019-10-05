def formatCSV():
    import csv
    with open('foods_output.csv', 'w') as outfile:
        with open('foods_input.csv', 'r') as infile:
            csv_reader = csv.reader(infile.read().splitlines())
            csv_writer = csv.writer(outfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            labels_row = writeCSVLabels(csv_reader) 
            csv_writer.writerow(labels_row)
            
            infile.seek(0)
            csv_reader = csv.reader(infile.read().splitlines())
            writeCSVRows(csv_reader, csv_writer, labels_row)


def writeCSVLabels(csv_reader):
    current_row = 1
    labels = []
    for row in csv_reader:
        if(current_row > 1 and len(row) > 5 and (row[4] != "") and (row[4] not in labels)):
            labels.append(row[4])
        current_row += 1
    labels.append('food')
    return labels

def writeCSVRows(csv_reader, csv_writer, labels_row):
    outfile_row = []
    current_row = 1
    for row in csv_reader:
        if(current_row > 1 and len(row) > 0):
            if(row[1] == "" and len(outfile_row) > 0):
                if((row[4] != "") and (row[4] in labels_row)):
                    ingredient_index = labels_row.index(row[4])
                    outfile_row[ingredient_index] = 1
            else:
                if(len(outfile_row) > 0):
                    csv_writer.writerow(outfile_row)    
                
                outfile_row = []
                for col in range(len(labels_row) -1):
                    outfile_row.append(0)
                outfile_row.append(row[1])
                
                if((row[4] != "") and row[4] in labels_row):
                    ingredient_index = labels_row.index(row[4])
                    outfile_row[ingredient_index] = 1
            
        current_row += 1
if __name__ == "__main__":
    formatCSV()