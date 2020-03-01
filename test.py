from collections import OrderedDict
COMPONENTS = [
    ('basic', 'Basic Environment(Docker, Python)'),
    ('xledger', 'xLedger Platform'),
    ('luna', 'Luna Platform')
]

od = OrderedDict()
for k, v in COMPONENTS:
    od[k] = v

print(list(od.values()))


