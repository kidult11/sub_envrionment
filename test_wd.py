#2025.4.23 tcp是同步函数
####功能函数备份2024.3.22

import struct  # struct 模块，用于处理二进制数据的转换。
import socket  #socket 模块，用于创建网络套接字和进行网络通信。
import pymysql
import sqlite3
# def get_db_connection():
#     conn = pymysql.connect(host='localhost', port=3306,user='root', passwd='123mysql', db='python_wendu')
#     #conn = pymysql.connect(host='192.168.0.106',port=1030, user='xinke', passwd='xinke606', db='python_wendu',charset='utf8')
#     return conn
#
# def load_saved_values(name):
#     #conn = pymysql.connect(host='localhost', user='root', passwd='123mysql', db='python_wendu')
#     #conn = pymysql.connect(host='192.168.0.106', user='xinke', passwd='xinke606', db='python_wendu')
#     conn = get_db_connection()
#     cur = conn.cursor()
#     try:
#         cur.execute("SELECT setting_value FROM admin_settings WHERE setting_name = %s", (name,))
#         result = cur.fetchone()
#         if result is not None and result[0] is not None:
#             return result[0]
#         else:
#             print(f"未在数据库中找到{name}的保存数据.")
#     except pymysql.MySQLError as e:
#         print(f'数据库操作出现错误: {e}')
#     finally:
#         conn.close()
#     return "Default Value"
#处理接收温湿度表数据
def jieshou_wd(a):
    arr1 = a.split()  # 按空格切割
    #地址 功能 字节数  温度值   湿度值    校验码
    #01   03    04   02 92   FF 9B   5A 3D
    num_dict = {'从机地址': arr1[0],
                '从机功能码': arr1[1],
                '字节数据': arr1[2],
                '湿度值': arr1[3:5], #3 4
                '温度值': arr1[5:7], #5 6
                '校验码':arr1[-2:]}  #7 8
    return num_dict
#接收水表
def jieshou_sb(a):
    arr1=a.split()
    num_dict = {'从机地址': arr1[0],
                '从机功能码': arr1[1],
                '字节数据': arr1[2],
                '用水量': arr1[3:7],
                '校验码': arr1[-2:-1]}
    return num_dict
# print(jieshow_sb('0B 03 04 00 07 00 00 E1 F2'))

# 新增烟雾传感器解析函数（统一数据结构）
#发送97  03   00 02 00 01 CRC
#发送97  03   00 00 00 01 CRC
#接受97 03 02 OD 7A CRC   OD7A为浓度值，16进制转为10进制
#接受97 03 02 00 01 CRC    0001为状态值，0001报警，0000正常
def jieshou_smoke(a):
    arr1 = a.split()

    num_dict = {
        "address": arr1[0],          # 设备地址
        "function_code": arr1[1],    # 功能码
        "data_length": arr1[2],     # 数据长度
        #"value": arr1[3] + arr1[4],  # 状态/浓度值（2字节）
        "value":arr1[3:5],
        "crc": arr1[-2:]            # CRC校验码
    }
    return num_dict


def jieshou_light(a):
    arr1=a.split()
    num_dict = {'从机地址': arr1[0],
                '从机功能码': arr1[1],
                '字节数据': arr1[2],
                '光照': arr1[3:7],
                '校验码': arr1[-2:-1]}
    return num_dict

#进行温湿度查询
def shidu(dict):
    list=dict['湿度值']
    str = ''.join(list)
    print("湿度值:" + str)
    float_num = int(str,16)
    print(float_num/10)
    return float_num/10
# shidu(jieshou_wd('15 03 04 02 01 00 C4 FF D9'))

#进行温度查询
def wendu(dict):
    list=dict['温度值']
    str = ''.join(list)
    print("温度值:"+str)
    float_num = int(str,16)
    print(float_num/10)
    return float_num/10
# wendu(jieshou_wd('15 03 04 02 01 00 C4 FF D9'))

def smoke(dict):
    """将16进制浓度值转为十进制（文档未定义单位，暂返回原始值）"""
    list = dict['value']
    str = ''.join(list)
    print("烟雾浓度值:" + str)
    float_num = int(str,16)
    return float_num

def is_smoke_alarm(dict):
    list = dict['value']
    str = ''.join(list)
    print("烟雾状态:" + str)
    return str

#进行查询用水量操作
def yongshui(dict):
    list=dict['用水量']
    str = ''.join(list)
    high_16=str[:4]
    low_16=str[4:]
    re_str=low_16+high_16
    print("用水量:"+re_str)
    num=int(re_str,16)
    print(num)
    return num
# a=jieshou_sb('0B 03 04 00 07 00 00 E1 F2')
# b=yongshui(a)
# print(b)

#进行查询光照操作
def light(dict):
    list=dict['光照']
    str = ''.join(list)
    high_16=str[:4]
    low_16=str[4:]
    re_str = high_16 + low_16
    print("光照:"+re_str)
    num=int(re_str,16)/1000
    print(num)
    return num
#校验码校验 校验通过返回1，校验未通过返回0 发送命令与接收命令通用
def jiaoyan_crc(data):
    poly = 0xA001  #设置多项式值，用于计算 CRC 校验码。
    crc = 0xFFFF #16位crc寄存器
    data1 = data.split() #将输入的数据按空格分割，得到一个列表 data1
    DATA=data1[:-2] #提取出除去最后两个元素的数据部分，用于计算 CRC 校验码
    data3=[int(x,16) for x in DATA]  #将十六进制字符串转换为对应的整数列表，这样方便后续的位操作。
    if not data1 or len(data1) < 2:  # 首先检查输入的数据是否为空或长度小于2
        return False
    num=data1[-2]+data1[-1] #将输入数据中的最后两个元素拼接成一个字符串，这是用于校验的 CRC 码
    for b in data3: #遍历
        crc ^= b    #异或
        for _ in range(8): #8个循环
            if (crc & 1): #判断 CRC 寄存器的最低位是否为 1。
                crc = (crc >> 1) ^ poly #如果最低位为 1，则右移一位并与多项式进行异或运算，否则只右移一位。
            else:
                crc >>= 1
    crc=crc.to_bytes(2, byteorder='little') #将 16 位 CRC 寄存器转换为字节对象，字节顺序为小端序。
    crc=crc[::-1] #将字节对象进行反转，变为大端序。
    CRC=(hex((crc[1]<<8) | crc[0])) #将两个字节组合成一个十六进制数，表示计算得到的 CRC 校验码。
    test=CRC[2:].upper() #将计算得到的 CRC 校验码转换为大写形式，并且去除前缀 0x。
    if test==num:
        print('校验通过')
        tf=1
    else:
        print('校验未通过')
        tf=0
    return tf

#tcp请求数据
def tcp(hex_data, TCP_IP, TCP_PORT):
    hex_data_bytes = bytes.fromhex(hex_data) #将输入的十六进制字符串 hex_data 转换为字节对象，这样可以方便地进行网络传输。
# 创建TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # 尝试连接到服务器
        sock.connect((TCP_IP, TCP_PORT))
        print("连接成功") # 连接成功后打印消息
        # 设置超时时间为2秒
        sock.settimeout(2)
        # 发送数据
        sock.sendall(hex_data_bytes)
        # 接收服务器响应
        response = sock.recv(1024)
        # 将每个字节转换为十六进制字符串形式，并在每个字节后添加空格
        hex_response = format(response[0], '02X') # 处理第一个字节
        for byte in response[1:-1]: #遍历
            hex_response += ' ' + format(byte, '02X') #在每个字节的十六进制字符串表示后面添加一个空格，并将其添加到 hex_response 字符串中。这样做是为了让每个字节的十六进制表示之间有空格分隔。
        hex_response += ' ' + format(response[-1], '02X') # 处理最后一个字节

        print("应答帧:", hex_response) # 打印接收到的响应数据

    except socket.timeout:
        print("超时：未收到服务器响应") # 超时时打印消息
        hex_response = "0" # 设置异常值

    except ConnectionRefusedError:
        print("连接失败：服务器拒绝连接") # 连接失败时打印消息
        hex_response = "0" # 设置异常值

    except Exception as e:
        print("连接失败：", e) # 连接过程中出现其他异常时打印消息
        hex_response = "0" # 设置异常值

    finally:
        # 关闭socket连接
        sock.close()

    return hex_response
# hex_data = '79 03 20 00 00 10 45 BE'
# TCP_IP = '192.168.1.253'
# TCP_PORT = 1031
# tcp(hex_data,TCP_IP,TCP_PORT)

#判断接收数据位数是否正确 用于电表 温度表 水表不适用与车位探测
def pd_weishu(str1,str2): #接收数据与发送数据
    a=str1.replace(' ','')[4:6]    #去掉空格，然后取出从索引位置 4 到 6 的子字符串
    b=str2.replace(' ','')[-6:-4]  #先去掉空格，然后取出倒数第 6 到倒数第 4 的子字符串
    if int(a,16)==int(b,16)*2:
        print('数据正常')
        return 1
    else:
        print('数据错误')
        return 0

#计算校验码
def crc(data):
    poly = 0xA001 #生成项，常用0xA001
    crc = 0xFFFF  # 16位crc寄存器
    data1 = data.split()
    data3 = [int(x, 16) for x in data1] # data1 中的每个十六进制字符串转换为对应的整数，得到一个新的列表 data3
    for b in data3:
        crc ^= b #异或
        for _ in range(8): #一个字节（8 位）有 8 次迭代，即进行 8 次移位操作
            if (crc & 1):  #为1时
                crc = (crc >> 1) ^ poly
            else:
                crc >>= 1
    crc = crc.to_bytes(2, byteorder='little') #CRC 寄存器的值转换为一个长度为 2 的字节对象，采用小端字节序
    crc = crc[::-1]  #翻转
    CRC = (hex((crc[1] << 8) | crc[0])) #两个字节合并为一个16进制
    test = CRC[2:].upper() #将 CRC 中从第三个字符（不包含索引为 2 的字符）到末尾的子字符串提取出来，并转换为大写字母。
    num_crc = ' '.join([test[i:i + 2] for i in range(0, len(test), 2)])#两个字符分割成一组，并用空格连接起来，得到 CRC 校验码的字符串形式。
    return num_crc

# 修正烟雾传感器问询帧生成函数（地址动态递增，功能码固定0x03），状态寄存器有两种，查询状态返回0000，浓度寄存器返回0002
#当我查询的时候这两种都需要查询，浓度状态返回给msg3_smoke,状态在查询的时候返回给msg2_smoke
#具体格式如下，地址码从97开始，重新更改逻辑
#发送97  03   00 02 00 01 CRC
#发送97  03   00 00 00 01 CRC
#接受97 03 02 OD 7A CRC   OD7A为浓度值，16进制转为10进制
#接受97 03 02 00 01 CRC    0001为状态值，0001报警，0000正常
def qqm_smoke(num1, register='0x0000'):#97 03 00 00 00 01 1D 90
    """
    生成烟雾传感器问询帧，支持状态（0x0000）和浓度（0x0002）寄存器查询
    num1: 传感器编号（1开始，地址=0x97 + (num1-1)）
    register: 寄存器地址（0x0000=状态，0x0002=浓度）
    """
    if num1 < 1:
        raise ValueError("传感器编号需≥1")
    #base_addr = 0x97  # 初始地址为0x97（十进制151）
    num_dz = 0x97
    if num1 == 1:
        print(hex(num_dz))
    else:
        for a in range(num1 - 1):
            num_dz = num_dz + 1
        # 拆分寄存器地址为两个字节（如0x0000→'00 00'，0x0002→'00 02'）
    reg_high = register[2:4]  # 取高字节
    reg_low = register[4:6]  # 取低字节
    register_str = f"{reg_high} {reg_low}"
    # 固定功能码0x03，寄存器数量0x0001
    data = f"{num_dz:02X} 03 {register_str} 00 01"
    num_crc = crc(data)  # 计算CRC校验码
    num_qqm = f"{data} {num_crc}"
    print('问询帧：', num_qqm)
    return num_qqm

#请求码的组合 15 03 00 00 00 02 C7 1F
def qqm_wd(num1,str1): #num1是现在选择的几号传感器
    # 功能区
    num_gnq = ' 00 00 00 02 '
    #地址码
    if str1=='查询':
        num_dz = 0x15
        if num1==1:
            print(hex(num_dz))
        else:
           for a in range(num1-1):
                    num_dz=num_dz+1
    else:
        num_dz=0x01
    #功能码
    if str1=='查询':
        num_gn='0x03'
    else:
        num_gn='0x06'
    #计算CRC校验码
    data=str(hex(num_dz))[-2:].upper()+' '+num_gn[-2:]+num_gnq
    num_crc=crc(data)
    #合成请求码并返回
    num_qqm=data+num_crc
    print('问询帧：',num_qqm)
    return num_qqm


def qqm_sb(num1,str1): #
    # 功能区
    num_gnq = ' 00 01 00 02 '
    #地址码
    if str1=='查询':
        num_dz = 0x0B
        if num1==1:
            print(hex(num_dz))
        else:
           for a in range(num1-1):
                    num_dz=num_dz+1
    else:
        num_dz=0x01

    #功能码
    if str1=='查询':
        num_gn='0x03'
    else:
        num_gn='0x10'
    hex_str=format(num_dz,'02X')#长度为 2 的十六进制
    #计算CRC校验码
    data=hex_str+' '+num_gn[-2:]+num_gnq
    num_crc=crc(data)
    #合成请求码并返回
    num_qqm=data+num_crc
    print('问询帧：',num_qqm)
    return num_qqm

def qqm_light(num1,str1): #
    # 功能区
    num_gnq = ' 00 02 00 02 '
    #地址码
    if str1=='查询':
        num_dz = 0x8D
        if num1==1:
            print(hex(num_dz))
        else:
           for a in range(num1-1):
                    num_dz=num_dz+1
    else:
        num_dz=0x01

    #功能码
    if str1=='查询':
        num_gn='0x03'
    else:
        num_gn='0x06'
    hex_str=format(num_dz,'02X')
    #计算CRC校验码
    data=hex_str+' '+num_gn[-2:]+num_gnq
    num_crc=crc(data)
    #合成请求码并返回
    num_qqm=data+num_crc
    print('问询帧：',num_qqm)
    return num_qqm

##4.27
#############################################################
def detect_devices(TCP_IP, TCP_PORT):
    count = 0  # 已找到的设备数量
    no_response = 0  # 连续无响应的设备数量

    for address in range(1, 256):  # 假设设备地址在 1-255 之间
        send_data = qqm_wd(address,'查询')  # 发送查询指令
        recv_data = tcp(send_data, TCP_IP, TCP_PORT)  # 发送TCP请求并接收响应

        # 判断接收到的数据是否为空或长度小于2
        if recv_data and len(recv_data) >= 2 and jiaoyan_crc(recv_data):
            no_response = 0  # 重置无响应计数器
            count += 1  # 设备数量加一
        else:
            no_response += 1  # 如果没有收到响应，增加无响应计数器

        if no_response >= 2:  # 如果连续两个设备都没有响应
            break   # 停止搜索

    return count  # 在循环结束后，返回总的设备数量

