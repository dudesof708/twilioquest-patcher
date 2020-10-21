from sys import platform
from os import getenv, listdir
from shutil import copyfile

if platform.startswith('linux') or platform == 'darwin':
    print("Linux and macOS aren't supported yet!")
    exit()

print('Searching for game install...')

supported_versions = ['3.1.35']
appdata = getenv('APPDATA')

if not appdata:
    print("I couldn't find where apps are installed on the system. Is this a modded Windows install?")
    exit()

folders = listdir(appdata)

def not_found():
    print("I couldn't find TwilioQuest installed. Try installing again or running the launcher?")
    exit()

if 'TwilioQuest' not in folders:
    not_found()

path = appdata + '\\TwilioQuest'
if 'releases' not in listdir(path):
    not_found()

path += '\\releases'
if 'stable' not in listdir(path):
    not_found()

path += '\\stable'
folders = [v for v in listdir(path) if v in supported_versions]

if len(folders) == 0:
    not_found()

path += f'\\{folders[-1]}'
if 'public' not in listdir(path):
    not_found()

path += '\\public'
if 'levels' not in listdir(path):
    not_found()

path += '\\levels'
folders = listdir(path)

if 'common' in folders:
    folders.remove('common')

def process_challenge(chal, innerText='`pwned by Gideon.`'):
    predef = 'module.exports = async'
    # copyfile(chal, f'{chal}.old')
    with open(chal, 'r') as f:
        tel = [x for x in f.readlines() if x.startswith('module.exports')][0]
        if 'helper' in tel:
            print(f'{predef} helper => ' + '{return helper.success(' + innerText + ');}')
        else:
            print(f'{predef} (context, callback) => ' + '{callback(null,' + innerText + ')}')

def process_category(path, challenges):
    for challenge in challenges:
        try:
            next_ch = f'{path}\\{challenge}'
            ch_files = listdir(next_ch)
            if 'validator.js' in ch_files:
                process_challenge(f'{next_ch}\\validator.js')
        except:
            pass

folders = [f'{path}\\{x}' for x in folders]
for folder in folders:
    files = listdir(folder)
    if 'objectives' in files:
        folder += '\\objectives'
        challenges = listdir(folder)
        if 'validation' in challenges:
            challenges.remove('validation')
        process_category(folder, challenges)