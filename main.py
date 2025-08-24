####ui设计最终版本2024/3/21 17：49
###数据库设计2024.3.27
##2024.3.28最后一版，可以绘图但是没有考虑时间和数据点，并且数据库的有些数据可能是乱的

###2024.4.7现在是将数据库里的100个数据全部绘图，当有了时间选择之后，则将选择时间范围内的数据全部绘图

####2024.4.9现在可以选择时间段数据
###4.23修改添加管理员登陆按钮
##4.24增加管理者/用户界面，实现来回跳界面
##4.26修改，现在能将管理者做的修改保存在数据库 ，并且下次打开显示管理员修改的东西
##5.9修改，改成了内网连接实验室数据库，但是网络问题还是怎样报错，接下来根据4.27的备份一步步修改
from tkinter import simpledialog
from tkinter.ttk import Combobox
from threading import Timer  # 需要导入Timer库
import pandas as pd
import time as tm
from tkinter import *
import os
import sys
from tkinter import Toplevel, Label, Entry, Button, StringVar
import pymysql

import tkinter as tk
from tkinter import ttk

from pymysql import Connection
from sqlalchemy import create_engine
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pandas.plotting import register_matplotlib_converters  # 追加这一行
from datetime import time
from datetime import datetime
from tkcalendar import DateEntry
from matplotlib.ticker import MaxNLocator
from tkinter import Tk, Label, Button, Scale, HORIZONTAL
from datetime import timedelta
import threading
from test_wd import *
import sqlite3
# 创建一个注册转换器
register_matplotlib_converters()  ## 注册转换器

root = tk.Tk()  # 主窗口
root.title('智能化展厅综合信息查询系统V2.0')

#root.geometry('600x500')  # 主窗口大小
# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 计算窗口的宽度和高度
window_width = 600
window_height = 500

# 计算窗口在屏幕上的位置
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

# 设置窗口的位置和大小
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
lb_bg = StringVar()  # 创建一个StringVar来保存标签背景颜色
lb_bg.set('#6495ED')  # 初始值设置为深蓝色
lb = tk.Label(root, text='环境监控平台', bg='#6495ED', fg='#ffffff', font=('黑体', 18), width=60, height=2)
lb.pack(fill='both')


def switch_to_home():
    lb_bg.set('#6495ED')  # 设置标签背景颜色为深蓝色
    page1.pack(fill='both', expand=True)
    page2.pack_forget()
    home_btn.config(bg='#6495ED')
    data_center_btn.config(bg='white')
def switch_to_data_center():
    lb_bg.set('white')  # 设置标签背景颜色为白色
    page1.pack_forget()
    page2.pack(fill='both', expand=True)
    home_btn.config(bg='white')
    data_center_btn.config(bg='#6495ED')

button_frame = Frame(root)
button_frame.pack(fill=X)
home_btn = Button(button_frame, text="首页", command=switch_to_home, bg='#6495ED', width=30)
home_btn.pack(side=LEFT)
data_center_btn = Button(button_frame, text="数据中心", command=switch_to_data_center, bg='white', width=30)
data_center_btn.pack(side=LEFT)
page1 = Frame(root)
page2 = Frame(root)
page1.pack(fill='both', expand=True)# 在这里添加其他代码, 并将所有的 "root" 替换为 "page1" 或 "page2"


# 示例：为 Label 添加边框
# lb7 = tk.Label(page1, text='秒', font=('华文新魏', 10), relief=tk.SOLID, borderwidth=1)
# lb7.place(relx=0.85, rely=0.12, relwidth=0.27, relheight=0.05)
####################################################################################################

lb7 = Label(page1, text='秒').place(relx=0.85, rely=0.12, relwidth=0.27, relheight=0.05)##首页的消息标签
lb8 = Label(page1, text='IP地址:').place(relx=0.11, rely=0.06, relwidth=0.1, relheight=0.05)
lb9 = Label(page1, text='端口:').place(relx=0.50, rely=0.06, relwidth=0.1, relheight=0.05)
comb2 = ttk.Combobox(page1, textvariable=StringVar, values=['115.236.153.172', '192.168.1.153','192.168.0.100'])
comb2.place(relx=0.2, rely=0.06, relwidth=0.3, relheight=0.05)
comb2.current(0)
comb3 = ttk.Combobox(page1, textvariable=StringVar, values=['14399', '40327', '1030'])
comb3.place(relx=0.59, rely=0.06, relwidth=0.15, relheight=0.05)
comb3.current(0)

lb10 = Label(page1, text='温度表编号:' ).place(relx=0, rely=0.13, relwidth=0.13, relheight=0.1)
lb11 = Label(page1, text='温度表地址:' ).place(relx=0, rely=0.24, relwidth=0.13, relheight=0.1)
lb12 = Label(page1, text='当前温度:').place(relx=0, rely=0.35, relwidth=0.13, relheight=0.1)
lb13 = Label(page1, text='当前湿度:').place(relx=0, rely=0.46, relwidth=0.13, relheight=0.1)
#lb21 = Label(page1, text='预留字段:' ).place(relx=0, rely=0.57, relwidth=0.13, relheight=0.1)
comb4: Combobox = ttk.Combobox(page1, textvariable=StringVar, values=[1, 2, 3, 4,5])
comb4.place(relx=0.15, rely=0.16, relwidth=0.08, relheight=0.05)
comb4.current(0)

lb18 = Label(page1, text='水表编号:').place(relx=0.27, rely=0.13, relwidth=0.13, relheight=0.1)
lb19 = Label(page1, text='水表地址:').place(relx=0.27, rely=0.24, relwidth=0.13, relheight=0.1)
lb20 = Label(page1, text='用水量:').place(relx=0.27, rely=0.35, relwidth=0.13, relheight=0.1)
lb23 = Label(page1, text='预留字段').place(relx=0.27, rely=0.46, relwidth=0.13, relheight=0.1)
#lb24 = Label(page1, text='预留字段:').place(relx=0.27, rely=0.57, relwidth=0.13, relheight=0.1)
comb6 = ttk.Combobox(page1, textvariable=StringVar, values=[1, 2])
comb6.place(relx=0.42, rely=0.16, relwidth=0.08, relheight=0.05)
comb6.current(0)

# 在 page1 的标签和输入框定义部分添加烟雾传感器
lb1_smoke = Label(page1, text='烟雾表编号:').place(relx=0.54, rely=0.13, relwidth=0.13, relheight=0.1)
lb2_smoke = Label(page1, text='烟雾表地址:').place(relx=0.54, rely=0.24, relwidth=0.13, relheight=0.1)
lb3_smoke = Label(page1, text='当前状态:').place(relx=0.54, rely=0.35, relwidth=0.13, relheight=0.1)
lb3_smoke = Label(page1, text='当前浓度:').place(relx=0.54, rely=0.46, relwidth=0.13, relheight=0.1)
#lb4_smoke = Label(page1, text='预留字段:').place(relx=0.54, rely=0.57, relwidth=0.13, relheight=0.1)
# 新增烟雾传感器编号选择框
comb_smoke = ttk.Combobox(page1, textvariable=StringVar, values=[1, 2, 3])  # 假设最多3个烟雾传感器
comb_smoke.place(relx=0.69, rely=0.16, relwidth=0.08, relheight=0.05)
comb_smoke.current(0)  # 默认选择1号传感器

lb1_light = Label(page1, text='光照表编号:').place(relx=0, rely=0.6, relwidth=0.13, relheight=0.1)
lb2_light = Label(page1, text='光照表地址:').place(relx=0, rely=0.71, relwidth=0.13, relheight=0.1)
lb3_light = Label(page1, text='光照强度:').place(relx=0, rely=0.82, relwidth=0.13, relheight=0.1)
comb_light = ttk.Combobox(page1, textvariable=StringVar, values=[1, 2, 3])  # 假设最多3个
comb_light.place(relx=0.15, rely=0.63, relwidth=0.08, relheight=0.05)
comb_light.current(0)  # 默认选择1号传感器

msg = '0.00'  # 信息将字符串赋值给msg
# Message创建消息框控件，放置在父窗口root中，width=80: 设置消息框控件的宽度为 80 个字符。fg='#8B8B7A': 设置消息框控件的前景色（文字颜色）为灰色。

# 温度表组件（全局变量）
global msg7, msg8, msg9, msg15
msg7 = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text='00 H')
msg7.place(relx=0.13, rely=0.24, relwidth=0.13, relheight=0.1)
msg8 = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text=msg)
msg8.place(relx=0.13, rely=0.35, relwidth=0.13, relheight=0.1)
msg9 = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text=msg)
msg9.place(relx=0.13, rely=0.46, relwidth=0.13, relheight=0.1)
#msg15 = tk.Message(page1, width=80, fg='#8B8B7A', text='/无')
#msg15.place(relx=0.13, rely=0.57, relwidth=0.1, relheight=0.1)
# 水表组件
global msg13, msg14, msg17, msg18
msg13 = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text='00 H')
msg13.place(relx=0.4, rely=0.24, relwidth=0.13, relheight=0.1)
msg14 = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text=msg )
msg14.place(relx=0.4, rely=0.35, relwidth=0.13, relheight=0.1)
msg17 = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text='/无')
msg17.place(relx=0.4, rely=0.46, relwidth=0.13, relheight=0.1)
#msg18 = tk.Message(page1, width=80, fg='#8B8B7A', text='/无')
#msg18.place(relx=0.4, rely=0.57, relwidth=0.1, relheight=0.1)
#地址，状态,浓度
global msg1_smoke, msg2_smoke, msg3_smoke, msg4_smoke
msg1_smoke = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text='00 H')
msg1_smoke.place(relx=0.67, rely=0.24, relwidth=0.13, relheight=0.1)

# 烟雾传感器状态显示
msg2_smoke = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text="无")  # 初始化状态显示FF0000红色
msg2_smoke.place(relx=0.67, rely=0.35, relwidth=0.13, relheight=0.1)
# 烟雾传感器浓度显示
msg3_smoke = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text="0")  # 初始化浓度显示0066FF蓝色
msg3_smoke.place(relx=0.67, rely=0.46, relwidth=0.13, relheight=0.1)
#msg4_smoke = tk.Message(page1, width=80, fg='#8B8B7A', text='/无')
#msg4_smoke.place(relx=0.67, rely=0.57, relwidth=0.13, relheight=0.1)
global msg_light_addr,msg_light_value
# 初始化界面时创建光照传感器相关标签
msg_light_addr = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text='00 H')  # 设备地址显示
msg_light_addr.place(relx=0.13, rely=0.71, relwidth=0.13, relheight=0.1)
msg_light_value = tk.Message(page1, width=80, fg='#8B8B7A',anchor=tk.W, text='0.00 Lux')  # 光照值显示
msg_light_value.place(relx=0.13, rely=0.82, relwidth=0.13, relheight=0.1)


######管理员界面
root.update()# 获取主窗口的大小和位置
root_width = root.winfo_width()
root_height = root.winfo_height()
root_x = root.winfo_rootx()
root_y = root.winfo_rooty()


def get_db_connection():
    # 获取程序所在目录（开发环境：脚本路径；打包环境：可执行文件路径）
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # 打包后路径
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # 开发环境路径
    db_path = os.path.join(base_path, 'data.db')  # 数据库路径与程序同目录

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def load_saved_values(name):
    #conn = pymysql.connect(host='localhost', user='root', passwd='123mysql', db='python_wendu')
    #conn = pymysql.connect(host='192.168.0.106', user='xinke', passwd='xinke606', db='python_wendu')
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        #SQL 查询使用 ? 作为参数占位符（原 MySQL 的 %s 需全部替换
        cur.execute('SELECT setting_value FROM admin_settings WHERE setting_name = ?', (name,))
        result = cur.fetchone()
        return result[0] if result else "Default Value"
    except sqlite3.Error as e:
        print(f"加载 {name} 失败：{str(e)}")
        return "Default Value"
    finally:
        cur.close()
        conn.close()


# 新建一个管理者登陆窗口
# 新建一个管理者登陆窗口
# 新建一个管理者登陆窗口
def admin_page():

    login_window = Toplevel()
    login_window.title("管理员登录")
    # 设置窗口置顶
    login_window.attributes('-topmost', True)
    # 设置新窗口的大小
    login_width = 250
    login_height = 120

    # 获取主窗口的大小和位置（移动到全局变量去了）
    pos_x = root_x + (root_width / 2) - (login_width / 2)  # 计算新窗口的位置
    pos_y = root_y + (root_height / 2) - (login_height / 2)
    # 设置新窗口的位置和大小
    login_window.geometry("%dx%d+%d+%d" % (login_width, login_height, pos_x, pos_y))

    # 创建用户名的标签和输入框
    username_var = StringVar()
    Label(login_window, text="用户名：").grid(row=0, padx=(20, 0), pady=(20, 0))
    Entry(login_window, textvariable=username_var, width=20).grid(row=0, column=1, padx=(0, 20), pady=(20, 0))

    # 创建密码标签和输入框
    password_var = StringVar()
    Label(login_window, text="密码：").grid(row=1, padx=(20, 0), pady=(20, 0))
    Entry(login_window, show='*', textvariable=password_var, width=20).grid(row=1, column=1, padx=(0, 20), pady=(20, 0))

    # 创建登录按钮，成功输入用户名密码之后进入到管理者设置页面
    def handle_login():
        # 获取用户名和密码
        username = username_var.get()
        password = password_var.get()
        # 连接到数据库
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # 查询用户名、密码匹配的用户及其权限
            cur.execute('''
                SELECT permission FROM admin_table
                WHERE username = ? AND password = ?
            ''', (username, password))
            result = cur.fetchone()
            if result:
                global current_user_permission
                current_user_permission = result['permission']
                print(f"登录用户权限：{current_user_permission}")
                # messagebox.showinfo("登录成功", "欢迎，你已成功登录！")
                login_window.destroy()
                switch_to_admin()
            else:
                # 暂时移除置顶属性
                login_window.attributes('-topmost', False)
                messagebox.showerror("登录失败", "用户名或密码错误，请重试。")
                # 恢复置顶属性
                login_window.attributes('-topmost', True)
        except sqlite3.Error as e:
            # 暂时移除置顶属性
            login_window.attributes('-topmost', False)
            messagebox.showerror("数据库错误", f"登录验证失败：{e}")
            # 恢复置顶属性
            login_window.attributes('-topmost', True)
        finally:
            conn.close()

    Button(login_window, text="登录", command=handle_login).grid(row=2, column=0, columnspan=2, sticky='w', padx=110)

    def close_login_window():
        login_window.destroy()
        # 如果主窗口被隐藏了，显示主窗口
        if root.state() == 'withdrawn':
            root.deiconify()

    login_window.protocol("WM_DELETE_WINDOW", close_login_window)



##page1上显示的管理者登录按钮，点击之后创建管理者登录界面，成功输入进入管理者设置
admin_button = Button(root, text='管理员登陆', relief=FLAT, bg="#6495ED", command=admin_page)
admin_button.place(relx=0.85, rely=0.025, relwidth=0.13, relheight=0.04)
##################################################################################################
##管理者设置界面
admin_window = None
def switch_to_admin():
    global admin_window, page21, page22
    lb_bg.set('#6495ED')
    admin_window = Toplevel()
    admin_window.title("管理员页面")
    admin_window.geometry("%dx%d+%d+%d" % (root_width, root_height, root_x, root_y))
    lb = tk.Label(admin_window, text='环境监控平台', bg='#6495ED', fg='#ffffff', font=('黑体', 18), width=60, height=2)
    lb.pack(fill='both')
    def admin_to_home():
        lb_bg.set('#6495ED')  # 设置标签背景颜色为深蓝色
        page21.pack(fill='both', expand=True)
        page22.pack_forget()
        home_btn.config(bg='#6495ED')
        data_center_btn.config(bg='white')
    def admin_to_data_center():
        lb_bg.set('white')  # 设置标签背景颜色为白色
        page21.pack_forget()
        page22.pack(fill='both', expand=True)
        home_btn.config(bg='white')
        data_center_btn.config(bg='#6495ED')
        # 添加/删除按钮权限控制（普通管理员禁用）


    button_frame = Frame(admin_window)
    button_frame.pack(fill=X)
    home_btn = Button(button_frame, text="设备管理", command=admin_to_home, bg='#6495ED', width=30)
    home_btn.pack(side=LEFT)
    data_center_btn = Button(button_frame, text="账号管理", command=admin_to_data_center, bg='white', width=30)
    data_center_btn.pack(side=LEFT)
    page21 = Frame(admin_window)
    page22 = Frame(admin_window)
    page21.pack(fill='both', expand=True)

####################################################################################################
####################################################################################################

    Label(page21, text='更改自动采集时间/秒：').place(relx=0, rely=0.05, relwidth=0.3, relheight=0.06)

    ##现在再次修改为可以显示之前修改的东西
    saved_time = load_saved_values('time')
    admin_input_var = StringVar(page21, saved_time if saved_time != "Default Value" else "5")
    admin_entry0 = ttk.Entry(page21, textvariable=admin_input_var) #输入框的更新自动保存
    admin_entry0.place(relx=0.25, rely=0.05, relwidth=0.1, relheight=0.06)
    #定时查询的时间，默认值是5s
    def update_time():
        global time_var
        input_text = admin_input_var.get()  # 读取输入
        if not input_text.isdigit():  # 检查输入是否为一个整数
            messagebox.showerror("错误", "输入不是有效的整数，请重新输入!")  # 如果不是，弹出错误提示框
            admin_input_var.set('')  # 清除输入框内容以便用户重新输入
        else:
            time_var.set(input_text)  # 如果输入是一个整数，更新首页的时间
            # 保存到数据库
            #conn = pymysql.connect(host='localhost', user='root', passwd='123mysql', db='python_wendu')
            #conn = pymysql.connect(host='192.168.0.106', user='xinke', passwd='xinke606', db='python_wendu')
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute('''
                      UPDATE admin_settings SET setting_value = ?
                      WHERE setting_name = 'time'
                  ''', (input_text,))
                conn.commit()
                print('定时时间设置已保存到数据库')
            except (ValueError, sqlite3.Error) as e:
                messagebox.showerror("错误", f"输入无效或保存失败：{str(e)}")
            finally:
                conn.close()
    # 新增按钮，点击后将输入框中的时间更新到首页
    btn_update_time = ttk.Button(page21, text="更新", command=update_time)
    btn_update_time.place(relx=0.35, rely=0.05, relwidth=0.1, relheight=0.06)

    ##########################################
    ##功能四四四报警温度界定
    ##########################################

    temp_limit_label = Label(page21, text="高温报警值/摄氏度：")
    temp_limit_label.place(relx=0.05, rely=0.75, relwidth=0.2, relheight=0.05)

    saved_temp_limit = load_saved_values('temp_limit')
    temp_limit_input_var = StringVar(page21, saved_temp_limit if saved_temp_limit != "Default Value" else "65")
    #
    temp_limit_entry0 = ttk.Entry(page21, textvariable=temp_limit_input_var)  # 输入框的更新自动保存
    temp_limit_entry0.place(relx=0.25, rely=0.75, relwidth=0.1, relheight=0.06)

    # 现在在数据库中查找保存的高温报警的值数，无则使用默认值65°C
    temp_limit_var = StringVar(page21, saved_temp_limit if saved_temp_limit != "Default Value" else "65")

    # # 新增按钮，点击后将输入框中将高温报警的温度进行更新
    def update_temp_limit():
        input_text = temp_limit_input_var.get()  # 读取输入
        try:
            val = float(input_text)  # 尝试将输入转换为浮点数临时的检查工具，以检验输入的合法性
            temp_limit_var.set(val)  # 如果转换成功
            # 保存到数据库
            conn = get_db_connection()
            cur = conn.cursor()
            try:
                cur.execute("UPDATE admin_settings SET setting_value = ? WHERE setting_name = 'temp_limit'",
                            (input_text,))
                conn.commit()
                print('高温报警数值设置已保存到数据库')
            except pymysql.MySQLError as e:
                print(f'数据库操作出现错误: {e}')
            finally:
                conn.close()
        except ValueError:  # 如果转换失败，将报 ValueError 错误
            messagebox.showerror("错误", "输入的不是有效的数字，请重新输入!")  # 弹出错误提示框
            temp_limit_input_var.set('')  # 清除输入框内容以便用户重新输入

    btn_update_temp_limit = ttk.Button(page21, text="更新", command=update_temp_limit)
    btn_update_temp_limit.place(relx=0.35, rely=0.75, relwidth=0.1, relheight=0.06)



######################################
    ##接下来写高温报警的函数
######################################
    def alarm():
        """温度超限时显示弹窗警告"""
        messagebox.showwarning("高温警报", "当前温度已超过阈值！")

    def check_and_update_high_temp(sensor_id, current_temperature, high_temp_limit):
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # 查询此传感器最新的一条超温记录（包含自增主键id）
            cur.execute(
                "SELECT id, sensor_id, time_limit_s, time_limit_e FROM temp_setting "
                "WHERE sensor_id = ? ORDER BY time_limit_s DESC LIMIT 1",
                (sensor_id,)
            )
            result = cur.fetchone()  # result 格式：(id, sensor_id, time_limit_s, time_limit_e)

            if current_temperature > high_temp_limit:
                if result:
                    # 直接使用DATETIME类型比较时间
                    if result[3] is None and datetime.now() - result[2] > timedelta(seconds=20):
                        alarm()  # 触发报警
                        time_stamp = datetime.now().replace(microsecond=0)  # 移除微秒（可选）
                        # 更新超温结束时间
                        cur.execute(
                            "UPDATE temp_setting SET time_limit_e = ? WHERE id = ?",
                            (time_stamp, result[0])  # 通过id更新记录
                        )
                        conn.commit()
                else:
                    # 插入新超温记录，id自动生成，time_limit_e为NULL
                    time_stamp = datetime.now().replace(microsecond=0)
                    cur.execute(
                        "INSERT INTO temp_setting (sensor_id, time_limit_s, time_limit_e) VALUES (?, ?, ?)",
                        (sensor_id, time_stamp, None)
                    )
                    conn.commit()
                    # 启动定时器，20秒后再次检查
                    t = Timer(20.0, check_and_update_high_temp, [sensor_id, current_temperature, high_temp_limit])
                    t.start()
            else:
                # 温度正常，若有未结束的超温记录，更新结束时间
                if result and result[3] is None:
                    time_stamp = datetime.now().replace(microsecond=0)
                    cur.execute(
                        "UPDATE temp_setting SET time_limit_e = ? WHERE id = ?",
                        (time_stamp, result[0])
                    )
                    conn.commit()
        except Exception as e:
            print("数据库执行错误: ", e)
        finally:
            conn.close()

    #def trigger_alert():#(这个函数要一直运行才行)## 触发警告函数（循环检测入口）
    # 在全局作用域添加监控状态变量
    global  monitoring
    monitoring = False
    global btn_monitor  # 用于引用监控按钮
    btn_monitor = None
    def trigger_alert():
        global monitoring
        if not monitoring:
            return  # 如果未开启监控，直接返回
        try:
            sensor_id = int(comb4.get())  # 温度id
            current_temperature = get_temperature()  # 获取当前温度
            conn = get_db_connection()  # 获取数据库连接
            cur = conn.cursor()
            try:
                # 执行SQL查询来获取'temp_limit'设定值
                cur.execute("SELECT setting_value FROM admin_settings WHERE setting_name = 'temp_limit'")
                result = cur.fetchone()
                if result is not None:
                    high_temp_limit = float(result[0])  # 找到了设定值，将其存储为浮点数
                else:
                    print("Cannot find 'temp_limit' in admin_settings table.")
                    return
            except Exception as e:
                print("Error executing the database query: ", e)
                return
            finally:
                conn.close()  # 在执行完查询后，不论其结果如何都要关闭数据库连接
            print(f'当前id：{sensor_id}')
            print(f'当前温度：{current_temperature}，设定警告温度：{high_temp_limit}')
            check_and_update_high_temp(sensor_id, current_temperature, high_temp_limit)
            # 递归调用实现循环监控（每5秒一次）
            if monitoring:  # 确保监控状态为True时继续调度
                root.after(5000, trigger_alert)
        except Exception as e:
            print("监控循环错误:", e)

    def toggle_monitoring():
        global monitoring, btn_monitor
        monitoring = not monitoring  # 切换监控状态
        if monitoring:
            btn_monitor.config(text="实时监控中")
            # 启动监控循环
            trigger_alert()
        else:
            btn_monitor.config(text="实时监控")
    btn_monitor = ttk.Button(page21, text="实时监控", command=toggle_monitoring)
    btn_monitor.place(relx=0.05, rely=0.85, relwidth=0.2, relheight=0.06)

    #################################################################################
    #################################################################################
    location_inputs = {}  # 创建一个字典用于存储所有的StringVar对象和Entry对象
    offset = 0.07  # 偏移量，你想要调整的数量
    for i in range(1, sensor_count + 1):
        var_temperature = tk.StringVar()
        var_temperature.set(f'温湿度传感器{i}：')
        label_temperature = tk.Label(page21, textvariable=var_temperature)
        label_temperature.place(relx=0, rely=i * 0.07+ offset, relwidth=0.3, relheight=0.06)

        # location_input_var = StringVar()
        # location_inputs[i] = {'var': location_input_var, 'entry': ttk.Entry(page21, textvariable=location_input_var)}
        # location_inputs[i]['entry'].place(relx=0.24, rely=i * 0.07+ offset, relwidth=0.2, relheight=0.06)
        ##现在修改为可以查数据库的值或者空，就是可以将输入的地方显示修改的值
        saved_location = load_saved_values(f'location{i}')  # 加载已经保存的位置
        location_input_var = StringVar(root, saved_location if saved_location != "Default Value" else '')
        location_inputs[i] = {'var': location_input_var, 'entry': ttk.Entry(page21, textvariable=location_input_var)}
        location_inputs[i]['entry'].place(relx=0.24, rely=i * 0.07 + offset, relwidth=0.2, relheight=0.06)

#######################################################
        def update_locations():
            #conn = pymysql.connect(host='localhost', user='root', passwd='123mysql', db='python_wendu')
            #conn = pymysql.connect(host='192.168.0.106', user='xinke', passwd='xinke606', db='python_wendu')
            conn = get_db_connection()
            cur = conn.cursor()
            for i in range(1, sensor_count + 1):
                input_location = location_inputs[i]['var'].get()  # 读取每个传感器的输入
                if input_location:  # 只有当有新的地址输入时才会执行更改操作
                    location_vars[i].set(input_location)  # 把输入的值赋给对应的location_var
                #
                # input_location = location_inputs[i]['var'].get()  # 读取每个传感器的输入
                # location_vars[i].set(input_location)  # 把输入的值赋给对应的location_var
                # 保存到数据库
                cur.execute("UPDATE admin_settings SET setting_value = ? WHERE setting_name = ?",
                            (input_location, f'location{i}'))
                conn.commit()
                print('设置已保存到数据库')
            conn.close()

        btn_update_location = ttk.Button(page21, text="更改所有地址", command=update_locations)
        btn_update_location.place(relx=0.24, rely=0.51, relwidth=0.15, relheight=0.06)



##第三部分，关于设备总数
##################################################################
    # 定义一个用于检测设备并弹出消息框的函数
    # 具体获取 TCP_IP, TCP_PORT 的方法根据你的界面设计而定
    device_count_label = Label(page21, text="")
    device_count_label.place(relx=0.30, rely=0.65, relwidth=0.2, relheight=0.05)
    # # 创建用于显示设备数量的标签，初始文本为空
    device_count_label1 = Label(page21, text="在线设备数：")
    device_count_label1.place(relx=0.23, rely=0.65, relwidth=0.12, relheight=0.05)

    #保存检测到的传感器数量
    save_btn = Button(page21, text="保存", state=DISABLED)  # 更新：添加保存按钮，初始状态为DISABLED
    save_btn.place(relx=0.48, rely=0.65, relwidth=0.1, relheight=0.05)

    # 创建一个线框
    line_frame = Frame(page21, height=1, bg="black")
    line_frame.place(relx=0.35, rely=0.7, relwidth=0.1)   # 更新：将线框宽度设置为标签和保存按钮的宽度总和

    def detect_devices_and_update_label():
        TCP_IP = comb2.get()
        TCP_PORT = int(comb3.get())
        count = detect_devices(TCP_IP, TCP_PORT)
        device_count_label.config(text=str(count))
        save_btn.config(state=NORMAL)  # 更新：检测结束后，把保存按钮设置为NORMAL

    def save_device_count():
        #conn = pymysql.connect(host='localhost', user='root', passwd='123mysql', db='python_wendu')
        #conn = pymysql.connect(host='192.168.0.106', user='xinke', passwd='xinke606', db='python_wendu')
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # cur.execute("INSERT INTO admin_settings (setting_name, setting_value) VALUES ('device_count', %s)",
            #             (device_count_label['text'],))
            cur.execute("UPDATE admin_settings SET setting_value = ? WHERE setting_name = 'device_count'",
                        (device_count_label['text'],))# 将设备数量保存到数据库
            conn.commit()
            print('保存设备数目完成')
            save_btn.config(state=DISABLED)  # 更新：保存完成后，把保存按钮设置为DISABLED
        except pymysql.MySQLError as e:
            print(f'数据库操作出现错误: {e}')
        finally:
            conn.close()

    def detect_and_show():
        device_count_label.config(text="检测中")
        save_btn.config(state=DISABLED)  # 更新：开始检测时，把保存按钮设置为DISABLED
        thread = threading.Thread(target=detect_devices_and_update_label, daemon=True)
        thread.start()

    # 更新：将保存按钮的命令设置为save_device_count
    save_btn.config(command=save_device_count)
    btn_detect = Button(page21, text="检测设备", command=detect_and_show)
    btn_detect.place(relx=0.07, rely=0.65, relwidth=0.13, relheight=0.05)


### 功能四，删减传感器
############################################################################


    def add_sensor():
        sensor_location = sensor_location_var.get()  # 获取输入框中的值
        if sensor_location:  # 如果输入框中有值
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM admin_settings WHERE setting_name LIKE 'location%'")
            next_sensor_id = cur.fetchone()[0] + 1
            cur.execute("INSERT INTO admin_settings (setting_name, setting_value) VALUES (?, ?)",
                        ('location' + str(next_sensor_id), sensor_location))
            conn.commit()
            messagebox.showinfo('信息', '成功添加传感器')  # 显示添加成功的消息
        else:  # 如果输入框中没有值
            messagebox.showwarning('警告', '请输入安装地址')  # 显示警告

    sensor_location_var = StringVar()  # 用于存储输入框中的值
    save_device_btn = Button(page21, text="增加传感器", command=add_sensor)
    save_device_btn.place(relx=0.55, rely=0.25, relwidth=0.13, relheight=0.05)
    Label(page21, text='安装地址：').place(relx=0.7, rely=0.25, relwidth=0.13, relheight=0.05)
    sensor_location_entry = Entry(page21, textvariable=sensor_location_var)
    sensor_location_entry.place(relx=0.83, rely=0.25, relwidth=0.13, relheight=0.05)

    def delete_sensor(sensor_id):
        conn = get_db_connection()
        cur = conn.cursor()
        # 检查该ID的传感器是否存在
        cur.execute("SELECT * FROM admin_settings WHERE setting_name=?", ('location' + str(sensor_id),))
        if cur.fetchone() is None:
            print("无法删除，因为找不到ID为 {} 的传感器".format(sensor_id))
            messagebox.showwarning('警告', '请输入需要删除的传感器')  # 显示警告
            return
        # 如果传感器存在则进行删除
        cur.execute("DELETE FROM admin_settings WHERE setting_name=?", ('location' + str(sensor_id),))
        conn.commit()
        print('成功删除传感器ID为 {} 的传感器'.format(sensor_id))
        messagebox.showinfo('信息', '成功删除传感器')  # 显示成功的消息

    def get_sensor_id_and_delete():
        sensor_id = sensor_id_var.get()
        delete_sensor(sensor_id)
    delete_detect = Button(page21, text="减少传感器", command=get_sensor_id_and_delete)
    delete_detect.place(relx=0.55, rely=0.35, relwidth=0.13, relheight=0.05)
    Label(page21, text='传感器编号：').place(relx=0.7, rely=0.35, relwidth=0.13, relheight=0.05)
    sensor_id_var = StringVar()
    sensor_id_entry = Entry(page21, textvariable=sensor_id_var)
    sensor_id_entry.place(relx=0.83, rely=0.35, relwidth=0.13, relheight=0.05)


    # =======================================================================================
    #超级管理原
    # 账号和密码输入框
    Label(page22, text="账号:").place(relx=0.25, rely=0.1, relwidth=0.1, relheight=0.06)
    username_entry = tk.Entry(page22)
    username_entry.place(relx=0.35, rely=0.1, relwidth=0.3, relheight=0.06)

    Label(page22, text="密码:").place(relx=0.25, rely=0.22, relwidth=0.1, relheight=0.06)
    password_entry = tk.Entry(page22, show="*")
    password_entry.place(relx=0.35, rely=0.22, relwidth=0.3, relheight=0.06)

    # 添加管理员函数（含权限校验）
    def add_admin():
        # 权限校验：非超级管理员无法执行
        if current_user_permission != '超级管理员':
            messagebox.showerror("权限不足", "只有超级管理员可添加账号！")
            return

        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showerror("错误", "请输入账号和密码！")
            return

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # 检查账号唯一性
            cur.execute("SELECT * FROM admin_table WHERE username = ?", (username,))
            if cur.fetchone():
                messagebox.showerror("错误", "账号已存在！")
                return

            # 获取权限等级（从下拉菜单获取）
            permission = permission_var.get()
            cur.execute(
                "INSERT INTO admin_table (username, password, permission) VALUES (?, ?, ?)",
                (username, password, permission)
            )
            conn.commit()
            messagebox.showinfo("成功", "管理员账号添加成功！")
        except pymysql.Error as e:
            messagebox.showerror("数据库错误", f"添加失败：{e}")
        finally:
            conn.close()

    # 删除管理员函数（含权限校验）
    def delete_admin():
        if current_user_permission != '超级管理员':
            messagebox.showerror("权限不足", "只有超级管理员可删除账号！")
            return

        username = username_entry.get()
        if not username:
            messagebox.showerror("错误", "请输入要删除的账号！")
            return

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            # 检查账号存在性
            cur.execute("SELECT * FROM admin_table WHERE username = ?", (username,))
            if not cur.fetchone():
                messagebox.showerror("错误", "账号不存在！")
                return

            cur.execute("DELETE FROM admin_table WHERE username = ?", (username,))
            conn.commit()
            messagebox.showinfo("成功", "管理员账号删除成功！")
        except pymysql.Error as e:
            messagebox.showerror("数据库错误", f"删除失败：{e}")
        finally:
            conn.close()

    # 权限下拉菜单（超级管理员可设置新账号权限）
    permission_var = tk.StringVar(value="普通管理员")
    Label(page22, text="权限等级:").place(relx=0.25, rely=0.35, relwidth=0.1, relheight=0.06)
    permission_dropdown = tk.OptionMenu(page22, permission_var, "超级管理员", "普通管理员")
    permission_dropdown.place(relx=0.35, rely=0.35, relwidth=0.3, relheight=0.06)

    # 添加/删除按钮（普通管理员时禁用按钮）
    add_button = tk.Button(page22, text="添加管理员", command=add_admin)
    add_button.place(relx=0.30, rely=0.5, relwidth=0.15, relheight=0.06)

    delete_button = tk.Button(page22, text="删除管理员", command=delete_admin)
    delete_button.place(relx=0.55, rely=0.5, relwidth=0.15, relheight=0.06)
    #==================================================================================================
    ###新增返回按钮
    return_button = Button(admin_window, text="返回", relief=FLAT, bg="#6495ED", command=switch_to_user)
    return_button.place(relx=0.02, rely=0.025, relwidth=0.1, relheight=0.04)
    ###隐藏原来的窗口
    # admin_window.protocol('WM_DELETE_WINDOW', close_admin) #关闭的是管理员窗口
    root.withdraw()
    admin_window.protocol('WM_DELETE_WINDOW', root.destroy)  # 点击“X”直接退出程序

# 定义回到用户状态的函数，包含激活用户窗口和关闭管理员窗口的操作
def switch_to_user():
    global admin_window
    if admin_window:
        admin_window.destroy()  # 销毁管理员窗口
    root.deiconify()  # 显示主窗口（如果之前被隐藏）

# 定义关闭管理员窗口的操作，包含激活用户窗口的操作
def close_admin():
    global admin_window
    root.deiconify()
    admin_window.destroy()


#现在在数据库中查找保存的时间，如果没有保存的时间，则使用默认值"5
saved_time = load_saved_values('time')
time_var = StringVar(root, saved_time if saved_time != "Default Value" else "5")

labeltime = ttk.Label(page1, textvariable=time_var)
labeltime.place(relx=0.92, rely=0.12, relwidth=0.055, relheight=0.05)

# 解析事件
def get_temperature():
    temp = None
    num_wd = int(comb4.get())
    TCP_IP = comb2.get()
    TCP_PORT = int(comb3.get())
    str_wd = qqm_wd(num_wd, '查询')
    crc_wd = jiaoyan_crc(str_wd)
    if crc_wd == 1:
        s_wd = tcp(str_wd, TCP_IP, TCP_PORT)
        if s_wd != '0' and pd_weishu(s_wd, str_wd) == 1:
            num_dict_wd = jieshou_wd(s_wd)
            temp = wendu(num_dict_wd)
    return temp

def Chaxun():
    # 将变量定义在 thread_func 函数的上一级作用域
    temp_success = False
    sb_success = False
    smoke1_success = False
    smoke2_success = False
    light_success =False
    def thread_func():
        nonlocal temp_success, sb_success, smoke1_success,smoke2_success,light_success
        num_wd = int(comb4.get())
        num_sb = int(comb6.get())
        TCP_IP = comb2.get()
        TCP_PORT = int(comb3.get())
        smoke_num = int(comb_smoke.get())
        num_light = int(comb_light.get())

        # ====================== 温度表查询 ======================
        str_wd = qqm_wd(num_wd, '查询')
        crc_wd = jiaoyan_crc(str_wd)
        if crc_wd == 1:
            s_wd = tcp(str_wd, TCP_IP, TCP_PORT)
            if s_wd != '0':
                if pd_weishu(s_wd, str_wd) == 1:
                    num_dict_wd = jieshou_wd(s_wd)
                    num_7 = str_wd[0:3] + 'H'
                    temp = wendu(num_dict_wd)
                    num_8 = str(temp) + '℃'
                    humidity = shidu(num_dict_wd)  # humidity
                    num_9 = str(humidity) + '%'
                    # 更新温度表界面（通过主线程）
                    root.after(0, lambda: [
                        msg7.config(text=num_7),
                        msg8.config(text=num_8),
                        msg9.config(text=num_9)
                    ])
                if save_flag:
                    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    conn = get_db_connection()
                    try:
                        cur = conn.cursor()
                        cur.execute('''
                            INSERT INTO save_data (id, time, wendu, shidu)
                            VALUES (?, ?, ?, ?)
                        ''', (num_wd, current_time, temp, humidity))
                        conn.commit()
                        print("数据保存成功")
                    except sqlite3.Error as e:
                        print(f"保存失败: {e}")
                        conn.rollback()
                    finally:
                        cur.close()
                        conn.close()
                temp_success = True

            elif s_wd == '0':
                print('连接错误')
                root.after(0, lambda: msg8.config(text="查询失败"))
                root.after(0, lambda: msg9.config(text="查询失败"))
                root.after(0, lambda: msg7.config(text="00 H"))


        # ====================== 水表查询 ======================
        str_sb = qqm_sb(num_sb, '查询')
        crc_sb = jiaoyan_crc(str_sb)
        if crc_sb == 1:
            s_sb = tcp(str_sb, TCP_IP, TCP_PORT)
            if s_sb != '0':
                if pd_weishu(s_sb, str_sb) == 1:
                    num_dict_sb = jieshou_sb(s_sb)
                    num_13 = str_sb[0:3] + 'H'
                    num_14 = yongshui(num_dict_sb)
                    print(num_dict_sb)
                    num_14 = str(num_14) + '立方米'
                    # 更新水表界面（通过主线程）
                    root.after(0, lambda: [
                        msg13.config(text=num_13),
                        msg14.config(text=num_14)
                    ])
                    sb_success = True
                else:
                    print('数据校验错误')
                    root.after(0, lambda: messagebox.showwarning("错误", "水表数据校验失败"))

            else:
                print('连接错误')
                root.after(0, lambda: msg13.config(text="00 H"))
                root.after(0, lambda: msg14.config(text="查询失败"))
        # ====================== 光照表查询 ======================
        str_light = qqm_light(num_light, '查询')
        crc_light = jiaoyan_crc(str_light)
        if crc_light == 1:
            s_light = tcp(str_light, TCP_IP, TCP_PORT)
            if s_light != '0':
                if pd_weishu(s_light, str_light) == 1:
                    num_dict_light = jieshou_light(s_light)
                    num_13 = str_light[0:3] + 'H'
                    num_14 = light(num_dict_light)
                    num_14 = str(num_14) + 'Lux'
                    # 更新光照界面（通过主线程）
                    root.after(0, lambda: [
                        msg_light_addr.config(text=num_13),
                        msg_light_value.config(text=num_14)
                    ])
                    light_success= True
                else:
                    print('数据校验错误')
                    root.after(0, lambda: messagebox.showwarning("错误", "光照表数据校验失败"))
            else:
                print('连接错误')
                root.after(0, lambda: msg_light_addr.config(text="00 H"))
                root.after(0, lambda: msg_light_value.config(text="查询失败"))

        # ====================== 烟雾传感器查询 ======================
        status_frame = qqm_smoke(smoke_num, '0x0000')
        status_response = tcp(status_frame, TCP_IP, TCP_PORT)
        if status_response != '0' and jiaoyan_crc(status_frame):
            if pd_weishu(status_response, status_frame):
                num_smoke_addr = status_frame[0:3] + 'H'
                #获得完整字段，类似于{'从机地址': '0B', '从机功能码': '03', '字节数据': '04', '用水量': ['00', '0B', '00', '00'], '校验码': ['21']}
                num_dict_smoke =jieshou_smoke(status_response)
                is_smoke_alarm(num_dict_smoke)
                # 更新状态显示（通过主线程）
                root.after(0, lambda: [
                    msg1_smoke.config(text=num_smoke_addr),
                    msg2_smoke.config(text="报警" if is_smoke_alarm == '0001' else "正常")
                ])
                smoke1_success = True
            else:
                print('数据校验错误')
                root.after(0, lambda: msg2_smoke.config(text="数据长度错误"))
        else:
            print('连接错误')
            root.after(0, lambda: msg1_smoke.config(text="00 H"))
            root.after(0, lambda: msg2_smoke.config(text="状态查询失败"))

        # 2. 查询浓度
        conc_frame = qqm_smoke(smoke_num, '0x0002')
        conc_response = tcp(conc_frame, TCP_IP, TCP_PORT)
        if conc_response != '0' and jiaoyan_crc(conc_frame):
            if pd_weishu(conc_response, conc_frame):
                #获得完整字段，类似于{'从机地址': '0B', '从机功能码': '03', '字节数据': '04', '用水量': ['00', '0B', '00', '00'], '校验码': ['21']}
                num_dict_smoke =jieshou_smoke(status_response)
                num_smoke_addr = status_frame[0:3] + 'H'
                concentration = smoke(num_dict_smoke)
                # 更新状态显示（通过主线程）
                root.after(0, lambda: [
                    msg1_smoke.config(text=num_smoke_addr),
                    msg3_smoke.config(text=concentration)
                ])
                smoke2_success = True
            else:
                print('数据校验错误')
                root.after(0, lambda: msg3_smoke.config(text="浓度数据错误"))
        else:
            print('连接错误')
            root.after(0, lambda: msg1_smoke.config(text="00 H"))
            root.after(0, lambda: msg3_smoke.config(text="浓度查询失败"))

        # ====================== 最终处理 ======================
        # 汇总错误信息
        errors = []
        if not temp_success: errors.append("温湿度表查询失败")
        if not sb_success: errors.append("水表查询失败")
        if not smoke1_success: errors.append("烟雾传感器状态查询失败")
        if not smoke2_success: errors.append("烟雾传感器浓度查询失败")
        if not light_success: errors.append("光照表查询失败")

        # 显示结果或错误
        root.after(0, lambda: [
            btn1.config(text="查询"),  # 恢复按钮状态
            #messagebox.showinfo("查询完成", "所有传感器查询完成") if not errors else
            #messagebox.showwarning("部分失败", "\n".join(errors))
        ])

        #恢复查询按键
        root.after(0, lambda: btn1.config(text="查询"))

    threading.Thread(target=thread_func, daemon=True).start()

def on_query_click():
    btn1.config(text="正在查询")
    root.after(0, Chaxun)

stop_task = True  # 初始设置为False，不执行任务
btn3 = None  # 全局变量用于引用定时查询按钮

def stop_periodic_task():
    global stop_task
    stop_task = True
    btn3.config(text="定时查询")  # 恢复按钮文本

def start_periodic_task():
    global stop_task
    stop_task = False
    btn3.config(text="定时查询中")  # 修改按钮文本
    periodic_task()

def periodic_task():
    global stop_task
    if stop_task:  # 检查标志
        return  # 如果是True, 则停止方法的执行
    try:
        time_set = int(time_var.get())  # 确保为整数
        Chaxun()
        root.after(time_set * 1000, periodic_task) # after(milliseconds, function)重新调度任务
    except ValueError:
        print("错误：时间设置必须为整数秒")
        stop_periodic_task()  # 停止任务并恢复按钮状态


btn_save = None# 新增全局变量 btn_save 用于引用保存按钮
save_flag = False
def click_save_button():
    global save_flag
    save_flag = not save_flag   # 点击保存按钮，save_flag值反转
    if save_flag:
        btn_save.config(text="正在保存")
        messagebox.showinfo("提示", "已开启数据保存功能，采集的数据将保存到数据库。")
    else:
        btn_save.config(text="保存")
        messagebox.showinfo("提示", "已关闭数据保存功能，采集的数据将不再保存到数据库。")
# 按钮
# command=Chaxun：指定了按钮被点击时要执行的函数为 Chaxun()

btn1 = Button(page1, text='查询', font=('华文新魏', 10), command=on_query_click)
btn1.place(relx=0.78, rely=0.06, relwidth=0.13, relheight=0.05)

btn3 = Button(page1, text='定时查询', font=('华文新魏', 10), command=start_periodic_task)
btn3.place(relx=0.78, rely=0.12, relwidth=0.13, relheight=0.05)

btn_stop = Button(page1, text='停止', font=('华文新魏', 10), command=stop_periodic_task)
btn_stop.place(relx=0.78, rely=0.18, relwidth=0.13, relheight=0.05)

btn_save = Button(page1, text='保存', font=('华文新魏', 10), command=click_save_button)
btn_save.place(relx=0.78, rely=0.24, relwidth=0.13, relheight=0.05)


def Qingchu():
    msg = '0.00'

    msg = '0.00'
    # 更新温度表组件文本
    msg7.config(text='00 H')
    msg8.config(text=msg)
    msg9.config(text=msg)
    #msg15.config(text='/无')
    # 更新水表组件文本
    msg13.config(text='00 H')
    msg14.config(text=msg)
    msg17.config(text='/无')
    #msg18.config(text='/无')
    # 更新烟雾传感器组件文本
    msg1_smoke.config(text='00 H')
    msg2_smoke.config(text="/无")
    msg3_smoke.config(text="0")
    #msg4_smoke.config(text='/无')
    msg_light_addr.config(text='00 H')
    msg_light_value.config(text=msg +' Lux')

btn2 = Button(page1, text='清除', font=('华文新魏', 10), command=Qingchu)
btn2.place(relx=0.78, rely=0.00, relwidth=0.13, relheight=0.05)


########页面2
########页面2
########页面2


# 在数据中心页面创建开始日期和结束日期的标签和输入框
# 创建开始日期和时间
start_date_label = tk.Label(page2, text='开始时间:')
start_date_label.place(relx=0.07, rely=0.42)
start_date_entry = DateEntry(page2, width=8, year=2024, month=4, day=3)
start_date_entry.place(relx=0.18, rely=0.42)
start_hour_entry = Spinbox(page2, from_=0, to=23, width=4)
start_hour_entry.place(relx=0.32, rely=0.42)

start_minute_entry = Spinbox(page2, from_=0, to=59, width=4)
start_minute_entry.place(relx=0.41, rely=0.42)

# 创建结束日期和时间
end_date_label = tk.Label(page2, text='结束时间:')
end_date_label.place(relx=0.57, rely=0.42)
end_date_entry = DateEntry(page2, width=8, year=2024, month=4, day=10)
end_date_entry.place(relx=0.68, rely=0.42)
end_hour_entry = Spinbox(page2, from_=0, to=23, width=4)
end_hour_entry.place(relx=0.82, rely=0.42)
end_minute_entry = Spinbox(page2, from_=0, to=59, width=4)
end_minute_entry.place(relx=0.91, rely=0.42)


# 获取开始和结束日期，然后将选中的日期、小时和分钟整合为一个日期和时间
start_date = start_date_entry.get_date()
start_time = time(hour=int(start_hour_entry.get()), minute=int(start_minute_entry.get()))
start_datetime = datetime.combine(start_date, start_time)

end_date = end_date_entry.get_date()
end_time = time(hour=int(end_hour_entry.get()), minute=int(end_minute_entry.get()))
end_datetime = datetime.combine(end_date, end_time)

sensor_count = 5  # 传感器数量
sensor_vars = []  # 初始化sensor_vars
# 颜色列表，用于不同的传感器绘图

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
canvas_container = tk.Frame(page2)
canvas_container.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.45)

location_vars = {}  # 暂存所有的location_var对象

#用户显示地址界面（新改的能够在输入框显示之前的值或空）
for i in range(1, sensor_count + 1):
    var_temperature = tk.StringVar()
    var_temperature.set(f'温湿度传感器{i}：')
    label_temperature = tk.Label(page2, textvariable=var_temperature)
    label_temperature.place(relx=0, rely=i * 0.07, relwidth=0.3, relheight=0.05)

    saved_location = load_saved_values(f'location{i}')
    location_vars[i] = StringVar(root, saved_location if saved_location != "Default Value" else f'默认地址{i}')
    label_location = ttk.Label(page2, textvariable=location_vars[i])
    label_location.place(relx=0.24, rely=i * 0.07, relwidth=0.2, relheight=0.05)


    var_temperature = tk.IntVar()

    chk_temperature = tk.Checkbutton(page2, text=f'温度{i}', variable=var_temperature)
    chk_temperature.place(relx=0.56, rely=i * 0.07, relwidth=0.1, relheight=0.05)

    var_humidity = tk.IntVar()
    chk_humidity = tk.Checkbutton(page2, text=f'湿度{i}', variable=var_humidity)
    chk_humidity.place(relx=0.7, rely=i * 0.07, relwidth=0.1, relheight=0.05)
    # Add the variable to the list
    sensor_vars.append((var_temperature, var_humidity))

# 创建一个空的图
fig = Figure(figsize=(5, 4), dpi=100)
ax1 = fig.add_subplot(111)
ax2 = ax1.twinx()
ax1.set_xlabel('Time')
ax1.set_ylabel('Temperature')
ax2.set_ylabel('Humidity')

canvas = FigureCanvasTkAgg(fig, master=canvas_container)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def plot_data():
    ax1.clear()
    ax2.clear()

    # 设置Y轴只显示最小值和最大值
    ax1.yaxis.set_major_locator(MaxNLocator(nbins=2))
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=2))

    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temperature')
    ax2.set_ylabel('Humidity')

    # 获取时间范围（新增有效性校验）
    try:
        start_date = start_date_entry.get_date()
        start_time = time(hour=int(start_hour_entry.get()), minute=int(start_minute_entry.get()))
        start_datetime = datetime.combine(start_date, start_time)

        end_date = end_date_entry.get_date()
        end_time = time(hour=int(end_hour_entry.get()), minute=int(end_minute_entry.get()))
        end_datetime = datetime.combine(end_date, end_time)

        if start_datetime > end_datetime:
            messagebox.showerror("错误", "开始时间不能晚于结束时间！")
            # 清空绘图
            ax1.clear()
            ax2.clear()
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Temperature')
            ax2.set_ylabel('Humidity')
            canvas.draw()
            return
    except Exception as e:
        messagebox.showerror("错误", "时间格式输入有误！")
        ax1.clear()
        ax2.clear()
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperature')
        ax2.set_ylabel('Humidity')
        canvas.draw()
        return

    checked_sensors = []
    for idx in range(1, sensor_count + 1):
        var_temp, var_hum = sensor_vars[idx - 1]
        if var_temp.get() == 1 or var_hum.get() == 1:
            checked_sensors.append(idx)

    if not checked_sensors:
        messagebox.showinfo("提示", "请至少勾选一个传感器的温度或湿度！")
        ax1.clear()
        ax2.clear()
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Temperature')
        ax2.set_ylabel('Humidity')
        canvas.draw()
        return

    has_temp_data = False  # 标记是否有温度数据
    has_hum_data = False  # 标记是否有湿度数据

    for idx in checked_sensors:
        var_temp, var_hum = sensor_vars[idx - 1]
        df = read_data_from_base(idx, start_datetime, end_datetime)
        if df.empty:
            messagebox.showinfo("提示", f"传感器 {idx} 在该时间段内无数据")
            ax1.clear()
            ax2.clear()
            ax1.set_xlabel('Time')
            ax1.set_ylabel('Temperature')
            ax2.set_ylabel('Humidity')
            canvas.draw()
            continue

        # 绘制温度曲线（如有勾选）
        if var_temp.get() == 1:
            ax1.plot(df['time'], df['wendu'], color=colors[idx % len(colors)],
                     label=f'Temp Sensor {idx}')
            has_temp_data = True  # 有温度数据

        # 绘制湿度曲线（如有勾选）
        if var_hum.get() == 1:
            ax2.plot(df['time'], df['shidu'], linestyle='--', color=colors[idx % len(colors)],
                     label=f'Hum Sensor {idx}')
            has_hum_data = True  # 有湿度数据


    # **关键修改：仅为有数据的轴绘制图例**
    if has_temp_data:
        ax1.legend(loc='upper left')  # 有温度数据时绘制温度图例
    if has_hum_data:
        ax2.legend(loc='upper right')  # 有湿度数据时绘制湿度图例

    # 时间轴设置
    ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate(rotation=45, ha='right')  # 旋转标签
    ax1.tick_params(axis='x', labelsize=8)  # 缩小字体大小

    canvas.draw()

def read_data_from_base(sensor_id, start_date, end_date):
    conn = get_db_connection()
    try:
        df = pd.read_sql_query('''
            SELECT time, wendu, shidu
            FROM save_data
            WHERE id = ? AND time BETWEEN ? AND ?
            ORDER BY time ASC
        ''', conn, params=(sensor_id, start_date, end_date))
        df['time'] = pd.to_datetime(df['time'])
        return df
    except sqlite3.Error as e:
        print(f"数据查询失败：{str(e)}")
        return pd.DataFrame()
    finally:
        conn.close()

btn_draw = Button(page2, text='绘图', font=('华文新魏', 10), command=plot_data)
btn_draw.place(relx=0.8, rely=0.01, relwidth=0.13, relheight=0.05)



# 初始化设置，连接数据库，并且检查是否存在这些数据库
def initialize_setting():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        # 创建管理员表（admin_table）
        cur.execute('''
                CREATE TABLE IF NOT EXISTS admin_table (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL,
                    permission TEXT DEFAULT '普通管理员'
                )
            ''')

        # 创建数据存储表（save_data）
        cur.execute('''
                CREATE TABLE IF NOT EXISTS save_data (
                    id INTEGER NOT NULL,
                    time DATETIME NOT NULL,
                    wendu REAL NOT NULL,
                    shidu REAL NOT NULL,
                    PRIMARY KEY (id, time)
                )
            ''')

        # 创建温度报警表（temp_setting）
        cur.execute('''
                CREATE TABLE IF NOT EXISTS temp_setting (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sensor_id INTEGER NOT NULL,
                    time_limit_s DATETIME NOT NULL,
                    time_limit_e DATETIME
                )
            ''')

        # 创建管理员设置表（admin_settings）
        cur.execute('''
                CREATE TABLE IF NOT EXISTS admin_settings (
                    setting_name TEXT PRIMARY KEY,
                    setting_value TEXT
                )
            ''')
        # 初始化管理员账号（首次运行时创建）
        cur.execute('SELECT COUNT(*) FROM admin_table')
        if cur.fetchone()[0] == 0:
            cur.execute('''
                  INSERT INTO admin_table (username, password, permission)
                  VALUES (?, ?, ?)
              ''', ('admin', 'admin123', '超级管理员'))
            conn.commit()
            # 初始化设置项（若不存在）
        settings = [
            ('time', '5'),
            ('temp_limit', '65'),
            ('device_count', '0')
        ]
        for setting in settings:
            cur.execute('''
                  INSERT OR IGNORE INTO admin_settings (setting_name, setting_value)
                  VALUES (?, ?)
              ''', setting)
            conn.commit()
        # 初始化传感器位置（location1-5）
        for i in range(1, 6):
            cur.execute('''
                INSERT OR IGNORE INTO admin_settings (setting_name, setting_value)
                VALUES (?, ?)
            ''', (f'location{i}', f'默认地址{i}'))
            conn.commit()

    except sqlite3.Error as e:
        messagebox.showerror("数据库错误", f"初始化失败：{str(e)}")
    finally:
        conn.close()
initialize_setting()

root.mainloop()
