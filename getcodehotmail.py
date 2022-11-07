import os,time
try:
 import threading,subprocess,base64,cv2,random,requests
 import numpy as np
except:
  os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
  os.system("pip install numpy")
import threading,subprocess,base64,cv2,random,requests
import numpy as np
from datetime import datetime

class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self,name):
        os.system(f"adb -s {self.handle} exec-out screencap -p > {name}.png ")
    def click(self,x,y):
        os.system(f"adb -s {self.handle} shell input tap {x} {y}")
    def DumpXML(self):
        name = self.handle
        if ":" in self.handle:
            name = self.handle.replace(":", "").replace(".", "")
        #print(name)
        os.system(f"adb -s {self.handle} shell uiautomator dump && adb -s {self.handle} pull /sdcard/window_dump.xml {name}.xml")
        return name+".xml"
    def find(self,img='',template_pic_name=False,threshold=0.99):
        if template_pic_name == False:
            self.screen_capture(self.handle)
            template_pic_name = self.handle+'.png'
        else:
            self.screen_capture(template_pic_name)
        img = cv2.imread(img)
        img2 = cv2.imread(template_pic_name)
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        test_data = list(zip(*loc[::-1]))
        return test_data

def get_code_hotmail(mail,pwd):
        code = requests.get(f'https://tools.dongvanfb.com/api/get_code?mail={mail}&pass={pwd}&type=instagram').json()["code"]
        return code
def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if len(p) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 0
GetDevices()
thread_count = len(GetDevices())
tk = open("tk.txt").readlines()
class starts(threading.Thread):
    def __init__(self, nameLD,file, i):
        super().__init__()
        self.nameLD = nameLD
        self.file = file
        self.device = i
    def run(self):
        email = self.file.split("|")[0]
        pwd = self.file.split("|")[1]
        #i = self.index
        device = self.device
        d = Auto(device)
        c = get_code_hotmail(email,pwd)
        print(c)

        


def main(m):
        device = GetDevices()[m]
        for i in range(m, len(tk), thread_count):
                mail = tk[i].strip()
                run = starts(device,mail, device,)
                run.run()

for m in range(thread_count):
    threading.Thread(target=main, args=(m,)).start()