import os, openpyxl, warnings, json
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

"""
Script to generate ru localization table
execute only in StreamingAssets folder!
"""

# check if right folder to run in
if os.getcwd().split('\\')[-1] != 'StreamingAssets':
    print('blyat')
    exit()

# load files
with open("localization.json", encoding='utf8') as f:
    localization = json.load(f)

# function to update files
def save_changes(isUpload=False):
    path = os.getcwd()
    wb = openpyxl.Workbook()
    ws = wb.create_sheet('Localization_ru')
    del wb['Sheet']
    ws.append(['Key','Русский'])
    # cleanup for upload
    if isUpload:
        for k in localization:
            ru = localization[k]['ru']
            if ru and ru.startswith('ඞ'):
                ru = ru[1:]
            ws.append([k,ru])
        wb.save(path + '\\Upload\\Localization_ru.xlsx')
    else: # amogus version for editing
        for k in localization:
            ws.append([k,localization[k]['ru']])
        wb.save(path + '\\OtherLocalization\\Localization_ru.xlsx')
    wb.close()

print('updating files')
save_changes(isUpload=False)
save_changes(isUpload=True)
print('done')
