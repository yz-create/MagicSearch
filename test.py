import json

with open('AtomicCards.json', 'r') as file:
    data = json.load(file)

type_lines = set()

for i in data['data']:
    for card in data['data'][i]:
        if 'type' in card:
            # Convertit toujours en chaîne
            value = card['type']
            if isinstance(value, list):
                value = " ".join(map(str, value))
            type_lines.add(value)

print(f"Nombre total de types uniques : {len(type_lines)}\n")
print("Liste complète des types :\n")

for t in sorted(type_lines):
    print(t)
