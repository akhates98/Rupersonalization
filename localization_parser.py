import os, openpyxl, warnings, json
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

"""
Script to update localization file
execute only in StreamingAssets folder!
"""

# check if right folder to run in
if os.getcwd().split('\\')[-1] != 'StreamingAssets':
    print('blyat')
    exit()

# load files
with open("localization.json", encoding='utf8') as f:
    localization = json.load(f)
with open('localization_backup.json', 'w', encoding='utf-8') as f:
    json.dump(localization, f, ensure_ascii=False)
with open("settings.json", encoding='utf8') as f:
    settings = json.load(f)

print('parsing files...')
# flag for updating
newStringsAdded = False
# parse folder and subfolders
for folder in os.walk(os.path.join(os.getcwd())):
    # filer non xlsx files
    tables = [x for x in folder[2] if x.startswith('Localization_')]
    path = folder[0]
    # for each file
    for t in tables:
        if t in settings['localization_file_list']['ignore']:
            continue
        print('checking',t)
        # load it
        fullpath = path + "\\" + t
        wb = openpyxl.load_workbook(fullpath)
        ws = wb.worksheets[0]
        # check if file is new
        if t not in settings['localization_file_list']['files']:
            newStringsAdded = True
            print('found new file: ', t)
            settings['localization_file_list']['files'].append(t)
        # iterate over rows starting with second one
        for key, cn, en, *values in ws.iter_rows(min_row=2, values_only=True):
            # check if not empty string
            if key == None:
                continue
            if en == None:
                en = ''
            # check if it's new string
            if key not in localization:
                newStringsAdded = True
                print('new string: ', t, key)
                localization[key] = {'files':[t],'cn':cn,'en':en,'ru':''}
            if localization[key]['en'] == None:
                localization[key]['en'] = ''
            # check if same key suddenly not appeared elsewhere
            if t not in localization[key]['files']:
                newStringsAdded = True
                print('string appeared in another file: ', t, key)
                localization[key]['files'].append(t)
            # check if there was change in en localization
            # bug: files may have different values of one key, but so far seems that translation is consistent
            #continue
            if en != localization[key]['en']:
                # doubles found:
                if key in ('易爆', '造成伤害', '1c6757aa97eb2a367697479776b9c18c', 'b3e80b2a4ec3fec39b9da30eaa3bc7b2','c44fd5492e9c0dfee96d7750597aaea9','44d61c38b0812f79231192d9417056e1'):
                    continue
                newStringsAdded = True
                print('found change for', key + ':', f"\"{localization[key]['en'].replace('\n',' ')}\""), '=>', f"\"{en.replace('\n',' ')}\""
                localization[key]['en'] = en
        # close file
        wb.close()

print('done')
if newStringsAdded:
    # update file if there was anything new
    with open('localization.json', 'w', encoding='utf-8') as f:
        json.dump(localization, f, ensure_ascii=False)