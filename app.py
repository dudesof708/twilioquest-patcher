from sys import platform
from os import getenv, listdir, remove
from shutil import copyfile
from argparse import ArgumentParser as parser
from re import sub

if platform.startswith('linux') or platform == 'darwin':
    print("Linux and macOS aren't supported yet!")
    exit()

print('Searching for game install...')

ar_parser = parser()
ar_parser.add_argument('-u', '--uninstall', help='uninstall hack', action='store_true', default=False)
args = ar_parser.parse_args()

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

def extract_success(lines, thi='helper.success'):
    begin = 0
    end = 0
    for i in range(len(lines)):
        if thi in lines[i]:
            begin = i
            for j in range(i, len(lines)):
                if ';' in lines[j]:
                    end = j
                    line = sub('\$\{(.*?)\}', '', ''.join(lines[i:j+1]).split(');')[0]) + ')'
                    line = sub('value: (.*?)(,| )', "value:'',", line)
                    line = sub('value: (.*?)}', "value:''}", line)
                    return line

def process_challenge(chal, innerText='`pwned by Gideon.`'):
    copyfile(chal, f'{chal}.old')
    line = ''
    with open(chal, 'r') as f:
        lines = [x.strip() for x in f.readlines()]
        tel = [x for x in lines if x.startswith('module.exports')][0]
        if 'helper' in tel:
            line = tel + extract_success(lines) + ';return;}'
        else:
            line = tel + extract_success(lines, 'callback(null') + ';return;}'
    with open(chal, 'w') as f:
        f.write(line)

def uninstall(f):
    try:
        copyfile(f'{f}.old', f)
        try:
            remove(f'{f}.old')
        except:
            pass
    except:
        pass

def process_category(path, challenges):
    for challenge in challenges:
        try:
            next_ch = f'{path}\\{challenge}'
            ch_files = listdir(next_ch)
            if 'validator.js' in ch_files:
                next_f = f'{next_ch}\\validator.js'
                if args.uninstall:
                    uninstall(next_f)
                elif 'validator.js.old' not in ch_files:
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

if args.uninstall:
    print('Successfully uninstalled hack.')
else:
    print('Successfully installed hack.')