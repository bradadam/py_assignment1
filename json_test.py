import json

d = [
    {"name": "test", "matric": "A12xx5678", "registered_courses": [], "total_credits": 0},
    ]


with open("students.json","w") as f:
    json.dump(d,f,indent=4)

with open("students.json","r") as f:
    data = json.load(f)
    print(data)