import serial
import serial.tools.list_ports
import time
import telnetlib
import requests
import json

# 检测串口
# 返回值 0串口检测通过， -1 无法打开串口, -2 设备串口异常
def testSerial(comname):
    # find port
    com = comname
    if comname == 0:
        return -1
    else:
        serialName = comname
    try:
        serialFd = serial.Serial(serialName, 9600, timeout=60)
        temp = serialFd.isOpen()
        if temp:
            print("serial port : ", serialFd.port, "\n")
        else:
            serialFd.open()
    except Exception as e:
        print(e)
        return -1

    i = 1
    while i < 5:
        print("bef serial write")
        serialFd.write('ok'.encode('utf-8'))
        print("after serial write")
        data = serialFd.read(2)
        while data == 'ok'.encode('utf-8'):
            print("Serial is ok \n")
            serialFd.close()
            return 0
        else:
            i = i + 1
            continue

    if i >= 5:
        print("Check serial fail\n")
        serialFd.close()
        return -2


#disk_check_report 结果: 0 全部正常, 1 SATA不正常, 2 USB不正常, 3 都不正常
def readfile(file_path):
    i = -1
    try:
        with open(file_path, 'r') as file:
            i = int(file.read())
    except Exception as e:
        print("read file_path fail:", e)
        return -1;

    if -1 == i:
        print('no checkfile\n')
        return i
    print('disk_check_report %d' % i)
    return i


def CheckDiskByTentel(devhost, user, pwd, finish, mountCmd):
    try:
        tn = telnetlib.Telnet(devhost, port=23, timeout=3)
    except Exception as e:
        print("Connect device timeout, 设备网络连接超时:", e)
        return -1

    #tn.set_debuglevel(2)
    tn.read_until(b'login: ')
    tn.write(user+b'\n')

    if (pwd != b''):
        tn.read_until(b'Password: ')
        tn.write(pwd+b'\n')
    tn.read_until(finish)

    #tn.write(b"mkdir /tmp/nkb/;mount -t nfs -o nolock 192.168.1.65:/c/nfsroot /tmp/nkb;\n")
    tn.write(mountCmd)
    tn.read_until(finish)

    tn.write(b"killall serial_echo;chmod +x /tmp/nkb/nkb_fac/serial_echo;/tmp/nkb/nkb_fac/serial_echo /dev/ttyAMA1 9600 &\n")
    tn.read_until(finish)
    tn.write(b"chmod +x /tmp/nkb/nkb_fac/disk_check_nkb.sh;/tmp/nkb/nkb_fac/disk_check_nkb.sh;cp /tmp/disk_check_report /tmp/nkb/nkb_fac/disk_check_report -f;sync;\n")
    tn.read_until(finish)
    #必须加延时 否则磁盘检测文件可能拷贝到电脑失败
    time.sleep(2)
    tn.close()
    return 0


def WriteAppByTentel(devhost, user, pwd, finish, mountCmd):
    try:
        tn = telnetlib.Telnet(devhost, port=23, timeout=3)
    except Exception as e:
        print("Connect device timeout, 设备网络连接超时:", e)
        return -1

    tn.set_debuglevel(2)
    tn.read_until(b'login: ')
    tn.write(user+b'\n')

    if (pwd != b''):
        tn.read_until(b'Password: ')
        tn.write(pwd+b'\n')
    tn.read_until(finish)

    #tn.write(b"mkdir /tmp/nkb/;mount -t nfs -o nolock 192.168.1.65:/c/nfsroot /tmp/nkb;\n")
    tn.write(mountCmd)
    tn.read_until(finish)

    t = str(int(time.time()))
    #strWriteFac = b"chmod +x /tmp/nkb/nkb_fac/3536d_nkb/fac/WriteFacInfo;/tmp/nkb/nkb_fac/3536d_nkb/fac/WriteFacInfo " + bytes(t, encoding="utf-8") + b'\n'
    strWriteFac = b"chmod +x /tmp/nkb/nkb_fac/3536d_nkb/fac/WriteFacInfo;cd /tmp/nkb/nkb_fac/3536d_nkb/fac/;./WriteFacInfo " + bytes(t, encoding="utf-8") + b'\n'
    print(type(strWriteFac))
    tn.write(strWriteFac)
    tn.read_until(finish)
    result = tn.read_very_eager()
    print(result.decode())

    #time.sleep(1)

    tn.write(b"rm /app/* -rf;cp /tmp/nkb/nkb_fac/3536d_nkb/app/* /app/ -rf;chmod 0777 /app/* -Rf;\n")
    tn.read_until(finish)
    result = tn.read_very_eager()
    print(result.decode())
    print("==== cp finish reboot dev====")
    tn.write(b"reboot\n")
    tn.read_until(finish)

    tn.close()
    return 0




def SetCustomMode(cus, devhost):
    http_url = 'http://' + devhost + '/Login.cgi'
    str1 = '{\"Header\":{\"Action\":\"Request\",\"Method\":\"SetIntellCustom\",\"Session\":\"\"},\"Param\":{\"Type\":'
    str2 = ',\"Reserve1\":\"192.168.1.115\",\"Reserve2\":\"rtsp://192.168.1.115:554/c=0&s=1\"}}\r\n\r\n'
    data = str1 + str(cus) + str2
    print(data)

    try:
        response = requests.post(http_url, data.encode('utf-8'), timeout=3)
        print(response.text)
        return response.text.find('OK')
    except Exception as e:
        print(e)
        return -1

