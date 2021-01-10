import psutil
def getProlist():
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name'])
        except psutil.NoSuchProcess:
            pass
        else:
            if "chromedriver.exe" in pinfo["name"]:
                return True,pinfo['pid']
    return False,0