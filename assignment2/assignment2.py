import csv
import os
import custom_module
from datetime import datetime

# Task 2:

def read_employees():

    try:
        myDict = {}
        myList = []

        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)

            for i, row in enumerate(reader):
                if i == 0:
                    myDict['fields'] = row
                else:
                    myList.append(row)

        myDict['rows'] = myList

        return myDict

    except Exception as e:
        print("Exception!")
        exit()


# Task 3:

def column_index(column_name):

    return employees['fields'].index(column_name)

employees = read_employees()
print(employees)

employee_id_column = column_index('employee_id')
print("ID column index: ", employee_id_column)


# Task 4:

def first_name(rowNum):

    index = column_index('first_name')
    row = employees['rows'][rowNum]
    
    return row[index]


# Task 5:

def employee_find(employee_id):

    def employee_match(row):

        return int(row[employee_id_column]) == employee_id
    
    matches = list(filter(employee_match, employees['rows']))

    return matches


# Task 6:

def employee_find_2(employee_id):
   
   matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
   
   return matches

# Task 7:

def sort_by_last_name():

    index = column_index('last_name')
    employees['rows'].sort(key=lambda row: row[index])

    return employees['rows']

# Task 8:

def employee_dict(row):

    data = {}

    for i in range(len(employees['fields'])):
        key = employees['fields'][i]
        if key == 'employee_id':
            continue
        value = row[i]
        data[key] = value
    
    return data

# Task 9:

def all_employees_dict():

    data = {}

    for row in employees['rows']:
        empId = row[employee_id_column]
        data[empId] = employee_dict(row)

    return data

# Task 10:

def get_this_value():

    return os.getenv('THISVALUE')

# Task 11:

def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)

set_that_secret('lalala')
print(custom_module.secret)

# Task 12:

def read_csv_to_minutes_dict(path):

    result = {}
    rows = []

    with open(path, 'r') as file:
        reader = csv.reader(file)

        for i, row in enumerate(reader):
            if i == 0:
                result['fields'] = row
            else:
                rows.append(tuple(row))

    result['rows'] = rows

    return result


def read_minutes():

    m1 = read_csv_to_minutes_dict('../csv/minutes1.csv')
    m2 = read_csv_to_minutes_dict('../csv/minutes2.csv')

    return m1, m2


minutes1, minutes2 = read_minutes()
print('Minutes 1: ', minutes1)
print('Minutes 2: ', minutes2)

# Task 13:

def create_minutes_set():

    set1 = set(minutes1['rows'])
    set2 = set(minutes2['rows'])

    return set1.union(set2)


minutes_set = create_minutes_set()
print('Combined set: ', minutes_set)

# Task 14:

def create_minutes_list():

    minutes_as_list = list(minutes_set)

    converted = map(lambda x: (x[0], datetime.strptime(x[1], '%B %d, %Y')), minutes_as_list)

    return list(converted)

minutes_list = create_minutes_list()
print('Minutes list with datetime: ', minutes_list)

# Task 15:

def write_sorted_list():

    sorted_list = sorted(minutes_list, key=lambda x: x[1])

    converted = list(map(lambda x: (x[0], x[1].strftime('%B %d, %Y')), sorted_list))

    with open('minutes.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(minutes1['fields'])

        for row in converted:
            writer.writerow(row)

    return converted

final_minutes = write_sorted_list()
print('Final: ', final_minutes)