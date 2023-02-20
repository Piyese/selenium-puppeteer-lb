import csv

with open('outputfin2.csv', mode= 'r') as odd_file:
    with open('outputfin3.csv', mode = 'a', newline='') as output:
        odd_reader = csv.reader(odd_file)
        profit = 0
        for row in odd_reader:

            prof = float(row[3])
            profit += prof
            row.append(round(profit, 2))
            odd_writer = csv.writer(output, delimiter=',')
            odd_writer.writerow(row)
            
