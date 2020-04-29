import serial
import serial.tools.list_ports
import nkb_test_function

def serialname1():
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <=0:
        print('无串口')
        b = [0]
        return b
    else:
        if len(plist) > 0:
            result = []
            for b in plist:
                result.append(str(b)[0:4])
            return result

def com(boxlist, setMsgLab):
    boxList = boxlist.get()
    if boxList == '无串口':
        setMsgLab("无串口", "red")
        nkb_test_function.testSerial(boxList)
        return 0
    elif boxList == 'COM1':
        setMsgLab("已选择串口COM1", "blue")
        return boxList
    elif boxList == 'COM2':
        setMsgLab("已选择串口COM2", "blue")
        return boxList
    elif boxList == 'COM3':
        setMsgLab("已选择串口COM3", "blue")
        return boxList
    elif boxList == "COM4":
        setMsgLab("已选择串口COM4", "blue")
        return boxList
    else:
        setMsgLab("已选择串口", "blue")
        return boxList

def testhost(host,setMsgLab):
    mountcmd1 = host
    mountcmd = 'mkdir /tmp/nkb/;''mount -t nfs -o nolock '
    mountcmd2 =':/c/nfsroot /tmp/nkb;\n'
    mountcmd3 = bytes(mountcmd+mountcmd1+mountcmd2,'utf-8') #字符串转字节
    print(len(mountcmd3))
    if len(mountcmd3) <= 61:
        setMsgLab("无地址", "red")
        return -0
    elif len(mountcmd3) <=74 and len(mountcmd3) >= 72:
        setMsgLab("已选择地址", "green")
        return mountcmd3
    else:
        setMsgLab("地址无效", "red")
        return -1









