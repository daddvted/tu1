from collections import OrderedDict
COMPONENTS = [
    ('basic', 'Basic Environment(Docker, Python)'),
    ('xledger', 'xLedger Platform'),
    ('luna', 'Luna Platform')
]

od = OrderedDict(COMPONENTS)

for k, v in od.items():
    print(f"{k} --- {v}")


