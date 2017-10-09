#!/usr/bin/evn python

import csv

def inches_to_meter(x):
    return x * 0.0254

def pounds_to_kilos(x):
    return x * 0.453592

def sanitize_string(x):
    return x.replace(" ","").lower()

def sanitize_height(x):
    sanitized_height = x
    #assume default in meter
    sanitized_height = sanitized_height.replace('m','')

    #is it explicitly in inches?
    is_in_inches = True if 'in' in sanitized_height else False
    sanitized_height = sanitized_height.replace('in','')
    #is empty?
    if len(sanitized_height) == 0:
        return None

    #print "%s %s" % (sanitized_height, is_in_inches)
    #get the number!
    try:
        height = float(sanitized_height)
    except:
        return None
    #check if the range is absurd
    is_in_inches = True if height > 2.5 else is_in_inches

    #convert if needed
    height = inches_to_meter(height) if is_in_inches else height
    return height

def sanitize_weight(x):
    sanitized_weight = x
    #assume default in kg
    sanitized_weight = sanitized_weight.replace('kg','')

    #is it explicitly in inces
    is_in_pounds = True if 'lb' in sanitized_weight else False

    sanitized_weight = sanitized_weight.replace('lb','')
    #is empty?
    if len(sanitized_weight) == 0:
        return None

    #print "%s %s" % (sanitized_weight, is_in_pounds)
    #get the number!
    try:
        weight = float(sanitized_weight)
    except:
        return None
    #check if the range is more complicated because is 0.45
    is_in_pounds = True if weight > 180 else is_in_pounds

    #convert if needed
    weight = pounds_to_kilos(weight) if is_in_pounds else weight
    return weight

def categorize(age, boundaries):
    #boundaries = [26, 36, 56, 56, 66, 76]
    final_category = len(boundaries)
    for category, upper_edge in enumerate(boundaries):
        #print category," ",upper_edge
        if age < upper_edge :
            final_category = category
            break
    return final_category

def compute_BMI(weight, height):
    if weight == None or height == None:
        return None
    return weight/(height **2)

with open("infile.csv",'r') as infile, open("outfile.csv",'w') as outfile:
    csvreader = csv.DictReader(infile)
    fieldnames = ['age','height', 'weight', 'age_class', 'BMI' , 'BMI_category']
    csvwriter = csv.DictWriter(outfile, fieldnames)
    csvwriter.writeheader()
    for line in csvreader:
        line['height'] = sanitize_height(line['height'])
        line['weight'] = sanitize_weight(line['weight'])
        age_boundaries = [26, 36, 56, 56, 66, 76]
        line["age_class"] = categorize(int(line['age']), age_boundaries)
        line['BMI'] = compute_BMI(line['weight'], line['height'])
        #print line['BMI']
        bmi_boundaries = [18.50001, 25, 30,40]
        bmi_names= ["thin", "healthy", "overweight", "obese", "high obese"]
        if line['BMI'] is not None :
            line["BMI_category"] =  bmi_names[categorize(line['BMI'], bmi_boundaries)]
        else:
            line["BMI_category"] = None
        csvwriter.writerow(line)
        #print
