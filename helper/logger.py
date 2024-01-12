import os
import platform
from datetime import datetime
from time import time

# typecheck
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import main

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class logger(object):
    def __init__(self, gui: "main.GUI"):
        os.system('cls' if os.name=='nt' else 'clear')
        self.printMode = gui.setting.DEBUG_PRINT
        self.debugMode = gui.setting.DEBUG_MODE
        self.clockingBuff: dict[str,float] = {}
        self.log = []
        self.log.append("-"*60)
        self.log.append(platform.platform())
        self.log.append(platform.processor())
        self.log.append(f"Python Version {platform.python_version()}")
        self.log.append("-"*60)
        self.log_dir = None
    
    def info(self, content: str):
        self.log.append(f"{bcolors.OKGREEN}[INFO] @{datetime.now()}{bcolors.ENDC} ---> {content}")
    
    def _check_log_dir_exist(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def timerStart(self, topic: str):
        self.clockingBuff[topic] = time()
    
    def timerEnd(self, topic: str):
        if topic in self.clockingBuff:
            self.info(f"{topic}: {bcolors.WARNING}{round((time()-self.clockingBuff[topic])*1000, 2)}{bcolors.ENDC} ms")
            del self.clockingBuff[topic]
        else:
            self.info(f"{topic} is not in the clocking buffer")
    
    def close(self):
        if self.debugMode:
            if self.printMode:
                for i in self.log:
                    print(i)
            elif not (len(self.log) == 4):
                if platform.system() == "Windows":
                    self.log_dir = os.getcwd()+'\\log'
                    self._check_log_dir_exist()
                    file = open(self.log_dir+f'\\{datetime.now().strftime("%H%M%S")}', 'w')
                else:
                    self.log_dir = os.getcwd()+'/log'
                    self._check_log_dir_exist()
                    file = open(self.log_dir+f'/{datetime.now().strftime("%H%M%S")}', 'w')
                self.log = [i+"\n" for i in self.log]
                file.writelines(self.log)
                file.close()