#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:ZhongHeyuan and SunXiaoFeng
#3536D网络键盘工厂工具

import time
import os
import numpy as np
from tkinter import *
import tkinter.messagebox as messagebox
import nkb_test_function
import serialname
import serial.tools.list_ports
#import serianametion
from tkinter import ttk


class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

        self.devHost = '192.168.1.90'
        #self.mountCmd = b'mkdir /tmp/nkb/;mount -t nfs -o nolock 192.168.1.56:/c/nfsroot /tmp/nkb;\n'
        self.file_path = 'C://nfsroot//nkb_fac//disk_check_report'

    def createWidgets(self):
        self.msgLabVarStr=StringVar()
        self.msgLabVarStr.set('准备开始检测！')
        self.msgLabVarStr2=StringVar()
        self.msgLabVarStr2.set('状态栏2')
        self.msgLabVarStr3 = StringVar()
        self.v = StringVar()
        self.v1 = StringVar()

        fmMsg = Frame(self.master)
        fmMsg.pack(side=TOP, anchor=W, fill=X, expand=YES, pady=10)
        self.msgLable=Label(fmMsg, textvariable=self.msgLabVarStr, bg='white', font=('Arial', 16), width=60, height=6)
        self.msgLable.pack(side=TOP, fill=NONE, expand=YES)
        self.msgLable2=Label(fmMsg, textvariable=self.msgLabVarStr2, bg='white', font=('Arial', 16), width=60, height=4)
        self.msgLable2.pack(side=TOP, fill=NONE, expand=YES)

        fmBtnFac = Frame(self.master)
        fmBtnFac.pack(side=TOP, anchor=W, fill=X, expand=YES, padx=12, ipadx=12, ipady=12)
        self.BtnTestDiskSerial = Button(fmBtnFac, text='1.检测磁盘和串口', command=self.testDiskAndSerial)
        self.BtnTestDiskSerial.pack(side=LEFT, fill=X, expand=NO, ipadx=4, ipady=11, padx=12)
        self.boxlist = ttk.Combobox(fmBtnFac, textvariable=self.v, state='readonly')  # 创建下拉菜单
        self.boxlist.pack(side=LEFT, anchor=W, fill=X, expand=NO, ipady=13)  # 设置下拉框的大小
        selfserialname = serialname.serialname1()
        res = []
        for i in selfserialname:
            res.append(i)  # 强制转换
        var = tuple(res)
        if var[0] == 0:
            self.boxlist['values'] = ("无串口")
            self.boxlist.current(0)
        else:
            self.boxlist['values'] = var
            self.boxlist.current(0)

        self.BtnWriteApp = Button(fmBtnFac, text='选择', activebackground="green",command=self.clickMe)
        self.BtnWriteApp.pack(side=LEFT, fill=X, expand=NO, ipadx=6, ipady=8, padx=6)
        self.e1 = Entry(fmBtnFac, textvariable=self.v1)         #创建一个输入框
        self.e1.pack(side=LEFT, fill=X, expand=YES, ipadx=12, ipady=12, padx=12)
        self.BtnBurnApp = Button(fmBtnFac, text='确认地址', activebackground="green",command=self.Host)
        self.BtnBurnApp.pack(side=LEFT, fill=X, expand=YES, ipadx=4, ipady=12, padx=5)

        fmBtnCus = Frame(self.master)
        fmBtnCus.pack(side=TOP, anchor=W, fill=X, expand=YES, pady=10, ipadx=8, ipady=8)
        self.BtnWriteApp = Button(fmBtnCus, text='2.烧写程序',activebackground="green", command=self.writeAppFacinfo)
        self.BtnWriteApp.pack(side=LEFT, fill=X, expand=YES, ipadx=12, ipady=12, padx=12)
        self.BtnModeTest = Button(fmBtnCus, text='测试模式', activebackground="green",command=self.setModeTest)
        self.BtnModeTest.pack(side=LEFT, fill=X, expand=YES, ipadx=12, ipady=12, padx=12)
        self.BtnCustomModeHYW = Button(fmBtnCus, text='客户定制1', activebackground="green",command=self.setModeHYW)
        self.BtnCustomModeHYW.pack(side=LEFT, fill=X, expand=YES, ipadx=12, ipady=12, padx=12)
        self.BtnCustomModeLS = Button(fmBtnCus, text='客户定制2', activebackground="green",command=self.setModeLS)
        self.BtnCustomModeLS.pack(side=LEFT, fill=X, expand=YES, ipadx=12, ipady=12, padx=12)
        self.BtnComplete = Button(fmBtnCus, text='重置工具',activebackground="green", command=self.checkComplete)
        self.BtnComplete.pack(side=LEFT, fill=X, expand=YES, ipadx=12, ipady=12, padx=12)

    def clickMe(self):
        com = serialname.com(self.boxlist,self.setMsgLab)
        print(com)
        return com

    def Host(self):
        self.host = self.e1.get()
        host = serialname.testhost(self.host,self.setMsgLab)
        print(host)
        self.mountCmd = host
        return self.host

    def testDiskAndSerial(self):
        self.setMsgLab("检测中", "yellow")
        print(self.mountCmd)
        retTelnet = nkb_test_function.CheckDiskByTentel(self.devHost, b'root', b'qwer1234', b' #', self.mountCmd)
        if -1 == retTelnet:
            self.setMsgLab("电脑与测试板网络连接失败！", "red")
            return -1

        retDisk = nkb_test_function.readfile(self.file_path)
        comName = serialname.com(self.boxlist, self.setMsgLab)
        retSerial = nkb_test_function.testSerial(comName)
        print("retDisk %d retSerial %d" % (retDisk, retSerial))

        if retSerial == -1:
            self.setMsgLab("电脑打开串口失败,请检查串口是否连接，或串口是否被占用！", "red")
            return -1
        elif retSerial == -2:
            self.setMsgLab2("解码板串口硬件异常，检测不合格!", "red")

        if 0 == retDisk:
            if 0 == retSerial:
                self.setMsgLab("SATA接口、USB接口、串口检测完毕，接口正常！\n请烧入程序（点击烧写程序按钮）", 'green')
                self.setMsgLab2("", 'green')
                return 0
            else:
                self.setMsgLab("SATA接口、USB接口接口正常！", 'green')
        elif 1 == retDisk:
            self.setMsgLab("SATA接口检测不合格!", "red")
        elif 2 == retDisk:
            self.setMsgLab("USB接口检测不合格!", "red")
        elif 3 == retDisk:
            self.setMsgLab("SATA接口、USB接口检测不合格!", "red")
        elif -1 == retDisk:
            self.setMsgLab("磁盘检测失败", "red")

        messagebox.showinfo('错误', '硬件检测不合格，建议硬件断电重新检测一次。\n重新检测仍失败标记问题检测其他硬件\n重新检测前点击重置工具')
        return -1



    def writeAppFacinfo(self):
        self.setMsgLab("程序烧入中", 'yellow')
        self.setMsgLab2("", "yellow")
        time.sleep(1)

        #/tmp/nkb/nkb_fac/3536d_nkb/fac/WriteFacInfo sec since 1970-1-1
        #cd /app/ko;/app/ko/load3536dv100 -a -total 512 -osmem 128;
        ret = nkb_test_function.WriteAppByTentel(self.devHost, b'root', b'qwer1234', b' #', self.mountCmd)
        if -1 == ret:
            self.setMsgLab("电脑与测试设备连接失败，请检查网络！", 'red')
        elif 0 == ret:
            self.setMsgLab("烧写成功，请断电重启设备。\n重启后检查屏幕和外接HDMI显示器是否有图像\n图像正常则全部功能检测通过", "green")
            self.setMsgLab2("点击重置工具后检测下一台设备", "green")
        #report = "写入成功 请查看屏幕"
        #messagebox.showinfo('烧写程序', '%s' % report)

    def checkComplete(self):
        try:
            if os.path.exists(self.file_path):
                print('remove file %s' % self.file_path)
                os.remove(self.file_path)
        except Exception as e:
            print("remove file fail:", e)
            messagebox.showinfo('message', '请手动删除文件 %s' % self.file_path)

        self.msgLable.configure(bg='white')
        self.msgLabVarStr.set("准备开始检测！")
        self.msgLable2.configure(bg='white')
        self.msgLabVarStr2.set("状态栏2")

    def setMsgLab(self, msg, bgc):
        self.msgLabVarStr.set(msg)
        self.msgLable.configure(bg=bgc)

    def setMsgLab2(self, msg, bgc):
        self.msgLabVarStr2.set(msg)
        self.msgLable2.configure(bg=bgc)

    def setModeTest(self):
        print("测试模式 TODO：send http msg")
        if (0 > nkb_test_function.SetCustomMode(0, self.devHost)):
            self.setMsgLab("设置 测试 模式失败", "red")
        else:
            self.setMsgLab("设置 测试 模式成功", "green")

    def setModeHYW(self):
        if (0 > nkb_test_function.SetCustomMode(1, self.devHost)):
            self.setMsgLab("设置 客户定制1 模式失败", "red")
        else:
            self.setMsgLab("设置 客户定制1 模式成功", "green")

    def setModeLS(self):
        if (0 > nkb_test_function.SetCustomMode(2, self.devHost)):
            self.setMsgLab("设置模式 客户定制2 模式失败", "red")
        else:
            self.setMsgLab("设置 客户定制2 模式成功", "green")

if __name__ == '__main__':
    app = Application()
    app.master.iconbitmap(default=r'graceport.ico')  # 更改默认图标
    app.master.title("恩港网络键盘测试工具V1.2")
    app.master.geometry("700x500")
    app.master.resizable(width=False, height=False)
    app.mainloop()
