import csv

input_file = open("/Users/connect/Downloads/tmp/k.csv")
reader_file = csv.reader(input_file)
value = len(list(reader_file))

print(value)