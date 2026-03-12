import json

with open('ucl_modules/module_api_response.json', 'r') as f:
    data = json.load(f)

modules = data['response']['Module_collection']['Module']

print(f'Total modules: {len(modules)}')
print('\nDepartments found:')
depts = {}
for m in modules:
    dept = m['ModuleContact']['Department']['DepartmentName']
    depts[dept] = depts.get(dept, 0) + 1

for d in sorted(depts.keys()):
    print(f'  {depts[d]:4d} - {d}')

