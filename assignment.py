#!/usr/bin/evn python
#   Assignment 10/10/17 Cognitive Systems
#   Team members (alphabetical order):
#   Mauro Comi, Eva Gil San Antonio,
#   Carlos Lopez Gomez, Giorgio Ruffa, Yirui Wang
#
import csv

def inches_to_meter(x):
    return x * 0.0254

def pounds_to_kilos(x):
    return x * 0.453592

#remove white spaces and put lowercase
def sanitize_string(x):
    return x.replace(" ","").lower()

#clear the height field, including interpretation of the possible unit of measure
#will return either a float expressed in meters or None
def sanitize_height(x):
    sanitized_height = x
    #maybe the user enterd "1.5m" or "1.6 m"
    #assume default in meter
    sanitized_height = sanitized_height.replace('m','')

    #is it explicitly in inches?
    #like "100in"
    is_in_inches = True if 'in' in sanitized_height else False
    sanitized_height = sanitized_height.replace('in','')
    #is empty?
    if len(sanitized_height) == 0:
        return None

    #get the number!
    #we use the exception to consider the encoding invalid
    try:
        height = float(sanitized_height)
    except:
        return None
    #check if the range is absurd
    #easier with inches, we do not need external factors
    is_in_inches = True if height > 2.5 else is_in_inches

    #convert if needed
    height = inches_to_meter(height) if is_in_inches else height
    return height

#clear the weight field, including interpretation of the possible unit of measure
#will return either a float expressed in kilograms or None
def sanitize_weight(x, age):
    sanitized_weight = x
    #assume default in kg
    sanitized_weight = sanitized_weight.replace('kg','')

    #is it explicitly in inces
    is_in_pounds = True if 'lb' in sanitized_weight else False

    sanitized_weight = sanitized_weight.replace('lb','')
    #is empty?
    if len(sanitized_weight) == 0:
        return None

    #get the number!
    try:
        weight = float(sanitized_weight)
    except:
        return None
    #check if the range is more complicated because is 0.45
    #
    is_in_pounds = True if weight > 200 else is_in_pounds

    #check for reasonable ranges using age
    #age is never null
    #As a rule of thumb we assume a liner relationship within age and weight
    #to draw the maximum reasonable weight in kilos for a given age
    #the formula is : max_kg_value = 7.76 * age + 6
    #6 is the maximum kg weight of a newborn (age=0)
    #7.76 is the slope of the line if a 25 year old man had a maximum weight of 200 kg
    if not is_in_pounds :
        is_in_pounds = True if weight > (7.76 * age + 6 )  else False


    #convert if needed
    weight = pounds_to_kilos(weight) if is_in_pounds else weight
    return weight

def categorize(age, boundaries):
    #boundaries = [26, 36, 56, 56, 66, 76]
    final_category = len(boundaries)
    #with enumerate the category is goin to range from 0 to (len(boundaries) -1)
    for category, upper_edge in enumerate(boundaries):
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
    #iterate over any line in the infile
    #every line is a map
    for line in csvreader:
        #clean and convert
        line['height'] = sanitize_height(line['height'])
        line['weight'] = sanitize_weight(line['weight'],int(line['age']))
        #categorize age
        age_boundaries = [26, 36, 56, 56, 66, 76]
        line["age_class"] = categorize(int(line['age']), age_boundaries)
        #compute BMI
        line['BMI'] = compute_BMI(line['weight'], line['height'])
        bmi_boundaries = [18.50001, 25, 30,40]
        bmi_names= ["thin", "healthy", "overweight", "obese", "high obese"]
        #assign a name to the BMI category
        if line['BMI'] is not None :
            line["BMI_category"] =  bmi_names[categorize(line['BMI'], bmi_boundaries)]
        else:
            line["BMI_category"] = None
        #write the new line one by one -> no need to keep the table in memory
        #using kernel and fs caching
        csvwriter.writerow(line)
        #print
