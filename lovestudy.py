from selenium import webdriver

from love_study_fun import vision
import signal
import close
import os


if __name__ == '__main__':
    print('''
        欢迎使用爱学教自动学习软件，
           使用方法详见说明，
      版本更新及其他问题请咨询给你软件的人，  
   ***本软件仅用于学习交流，切勿用于商业用途。***
   ''')
    # 打包时解封
    isServerOn, pid = close.getProlist()
    if isServerOn:
        print("清除残留进程")
        os.kill(pid, signal.SIGINT)
    try:
        vision(input("请输入您的账号："))
    except Exception as e:
        webdriver.Chrome().close()
        print(f"程序错误,请重新开始")
