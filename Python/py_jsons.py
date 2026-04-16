# json.loads() → JSON string to Python object
# json.dumps() → Python object to JSON string
# json.load() → JSON file to Python object
# json.dump() → Python object to JSON file
import json
sample_json_str = '''
{
  "emp_id": 101,
  "name": "Alice",
  "age": 30,
  "is_active": true,
  "skills": ["Python", "SQL", "PySpark"],
  "address": {
    "city": "Hyderabad",
    "state": "Telangana"
  },
  "projects": [
    {"project_name": "Retail ETL", "duration_months": 6},
    {"project_name": "Fraud Analytics", "duration_months": 9}
  ]
}
'''
# Convert JSON string to Python object
employee_data = json.loads(sample_json_str)
print(employee_data)
print(type(employee_data))  
# Convert Python object back to JSON string
json_string = json.dumps(employee_data, indent=4)   
print(json_string)


print("**********************************************")

s = '{"flag": true, "value": null, "nums": [1, 2, 3]}'
data = json.loads(s)

print(data)
print(type(data))
print(type(data["flag"]))
print(type(data["value"]))