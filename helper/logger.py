import os
import platform
from datetime import datetime

class logger(object):
    def __init__(self):
        self.log = []
        self.log.append(platform.platform())
        self.log.append(platform.processor())
        self.log.append(f"Python Version {platform.python_version()}")
        self.log.append("-----")
        self.log_dir = None
    
    def _log(self, content: str):
        self.log.append(f"{datetime.now()}: {content}")
    
    def _check_log_dir_exist(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def _close(self):
        if not (len(self.log) == 4):
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