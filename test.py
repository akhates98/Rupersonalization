import json

all = {}
with open("localization.json", encoding='utf8') as f:
    localization = json.load(f)

for k in localization:
    if "Localization_MOWUGUIYIZHE.xlsx" in localization[k]['files']:
        all[k] = localization[k]
with open('all.json', 'w', encoding='utf-8') as f:
    json.dump(all, f, ensure_ascii=False)