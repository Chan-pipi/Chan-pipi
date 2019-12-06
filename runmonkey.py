# -*- coding: utf-8 -*-
import time, os
execcount = 3
phone = "91QECNK27UM2"
monkeyclickcount = 100000
WORKSPACE = os.path.abspath(".")
def getWorkConfig():
    f = open("./.config", "r", encoding="UTF-8")
    config = {"phone": phone, "monkeyclickcount": monkeyclickcount, "execcount": execcount}
    try:
        while True:
            line = f.readline()
            if line:
                line = line.strip()
                linesplit = line.split("：")
                if linesplit.__sizeof__() > 1:
                    if linesplit[0] == 'phone':
                        config['phone'] = linesplit[1]
                    elif linesplit[0] == 'monkeyclickcount':
                        config["monkeyclickcount"] = linesplit[1]
                    elif linesplit[0] == 'execcount':
                        config["execcount"] = linesplit[1]
            else:
                break
    finally:
        f.close()
        print("config : %s" % config)
        return config
def installApk(config):
    phoneAddr = config.get("phone")
    print('Ready to start installing apk')
    if phoneAddr:
        installPhoneApk = "adb -s %s install -r %s\\apk\\ky_20190702_4.apk" % (phoneAddr, WORKSPACE)
        os.popen(installPhoneApk)
        print("install phone apk done")
def killTestApp():
    forceStopApp = "adb -s %s shell am force-stop com.kaiyuan.developmentbusiness" % workConfig.get('phone')
    os.popen(forceStopApp)
def createBugreport():
    print("create bugreport file")
    bugreport = "adb -s %s shell bugreport > %s\\bugreport.txt" % (workConfig.get("phone"), WORKSPACE)
    os.popen(bugreport)
    print("create bugreport file ,done")
    chkbugreport = "java -jar %s\\chkbugreport.jar %s\\bugreport.txt" % (WORKSPACE, WORKSPACE)
    os.popen(chkbugreport)
def fullmonkey(workconfig):
    killTestApp()
    openAgain = "adb -s %s shell am start com.kaiyuan.developmentbusiness/.weex.WeexActivity" % workconfig.get('phone')
    print(openAgain)
    os.popen(openAgain)
    monkeycmd = "adb -s %s shell monkey -p com.kaiyuan.developmentbusiness -v -v -v 100000" \
                "--ignore-timeouts --ignore-crashes --kill-process-after-error " \
                "--pct-touch 35 --pct-syskeys 30 --pct-appswitch 35 --hprof  " \
                "--throttle 100  %s" \
                % (workconfig.get("phone"), workConfig.get("monkeyclickcount"))
    os.popen(monkeycmd)
if __name__ == '__main__':
    workConfig = getWorkConfig()
    # installApk(workConfig)
    forcount = int(workConfig.get("execcount"))
    for i in range(forcount):
        print("execute monkey ,loop = %s" % (i + 1))
        fullmonkey(workConfig)
    createBugreport()
    print("Completion of the current round of testing")
