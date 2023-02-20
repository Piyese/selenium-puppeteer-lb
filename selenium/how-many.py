import csv

bank = 1000
last = ''
count = 0
with open('outputfin3.csv', mode='r') as file:
    content = csv.reader(file)
    for row in content:
        if last == 'red':
            last = row[4]
            continue
        elif count > 1:
            count = 0
            last = row[4]
            continue
        elif last == 'green' or last == 'purple':
            bank -= 10
            if float(row[2]) >= 3:
                bank += 20
                count += 1
        else: 
            print('ERROR!!!')
        last = row[4]
    
    print(bank)
        
    # print(f'red:{red}, purple: {purple}, green: {green}')