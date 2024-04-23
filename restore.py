import os, openpyxl, json
# check if right folder to run in
if os.getcwd().split('\\')[-1] != 'StreamingAssets':
    print('blyat')
    exit()

dump = {}
files = []
# parse folder and subfolders
for folder in os.walk(os.path.join(os.getcwd())):
    # filer non xlsx files
    tables = [x for x in folder[2] if x.startswith('Localization_')]
    path = folder[0]
    # for each file
    for t in tables:
        files.append(t)
        fullpath = path + "\\" + t
        wb = openpyxl.load_workbook(fullpath)
        ws = wb.worksheets[0]
        for key, cn, en, tcn, jp, kr, pt, ru, *values in ws.iter_rows(min_row=2, values_only=True):
            if key not in dump:
                dump[key] = {'files':[t],'en':en,'ru':ru}
            else:
                dump[key]['files'].append(t)
dump['localization_file_list'] = {'files': files}
with open('language_dump.json', 'w', encoding='utf-8') as f:
        json.dump(dump, f, ensure_ascii=False)
