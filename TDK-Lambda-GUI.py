import tkinter as tk
import socket
import time

# 建立tkinter窗口，设置窗口标题
top = tk.Tk()
top.title("TDK-Lambda 电源控制软件 v0.1 by r9T")
top.maxsize(480, 504)
top.minsize(400, 420)

# 可配置的UDP连接相关组件
# 创建UDP连接相关标签
label_UDPDSetup = tk.Label(top, text="建立UDP连接:").grid(row=0, column=0, sticky="W")
label_HostIP = tk.Label(top, text="输入电源IP地址").grid(row=1, column=1, sticky="W")
label_Port = tk.Label(top, text="输入端口号(8005)").grid(row=2, column=1, sticky="W")

# 创建UDP连接相关文本框
HostIP = tk.Entry(top)
Port = tk.Entry(top)

HostIP.grid(row=1, column=2, sticky="W")
Port.grid(row=2, column=2, sticky="W")

# 创建建立UDP连接按钮
def btnUDPsock():
    HOST = HostIP.get()  # 192.168.1.31
    PORT = int(Port.get())
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((HOST, PORT))


btnUDP = tk.Button(top, text="建立UDP连接", command=btnUDPsock).grid(row=3, column=1, sticky="W")

# 初始化设置相关组件
# 创建初始化设置相关标签
label_Init = tk.Label(top, text="初始化设置：").grid(row=4, column=0, sticky="W")
label_VOLT_Min = tk.Label(top, text="设置电压下限(V)").grid(row=5, column=1, sticky="W")
label_VOLT_Max = tk.Label(top, text="设置电压上限(V)").grid(row=6, column=1, sticky="W")
label_CURR_Limit = tk.Label(top, text="设置限流(A)").grid(row=7, column=1, sticky="W")
label_VOLT_ = tk.Label(top, text="设置正常工作电压(V)").grid(row=8, column=1, sticky="W")

# 创建初始化设置相关文本框
VOLT_Min = tk.Entry(top)
VOLT_Max = tk.Entry(top)
CURR_Limit = tk.Entry(top)
VOLT = tk.Entry(top)

VOLT_Min.grid(row=5, column=2)
VOLT_Max.grid(row=6, column=2)
CURR_Limit.grid(row=7, column=2)
VOLT.grid(row=8, column=2)

# 创建发送初始化设置按钮
def btnInitClicked():
    sock.send(bytes("OUTP:STAT 0", encoding='utf-8'))
    time.sleep(3)
    sock.send(bytes("OUTP:STAT 1", encoding='utf-8'))
    time.sleep(0.5)
    # 设置电压上下限
    sock.send(bytes(":VOLT:PROT:LEV " + VOLT_Max.get(), encoding='utf-8'))
    time.sleep(0.5)
    sock.send(bytes(":VOLT:LIM:LOW " + VOLT_Min.get(), encoding='utf-8'))
    time.sleep(0.5)
    # 设置限流
    sock.send(bytes(":CURR " + CURR_Limit.get(), encoding='utf-8'))
    time.sleep(0.5)
    # 设置正常工作的输出电压
    sock.send(bytes(":VOLT " + VOLT.get(), encoding='utf-8'))
    time.sleep(0.5)

btnInit = tk.Button(top, text="发送初始化设置", command=btnInitClicked).grid(row=9, column=1, sticky="W")

def btnSetVoltClicked():
    sock.send(bytes(":VOLT " + VOLT.get(), encoding='utf-8'))

btnSetVolt = tk.Button(top, text="设置电源输出电压", command=btnSetVoltClicked).grid(row=9, column=2, sticky="W")



# 创建循环测试相关组件
# 创建循环测试相关标签
label_LoopTest = tk.Label(top, text="循环测试设置：").grid(row=10, column=0, sticky="W")
label_Volt1 = tk.Label(top, text="设置电压1(V)").grid(row=11, column=1, sticky="W")
label_Time1 = tk.Label(top, text="设置持续时间1(S)").grid(row=12, column=1, sticky="W")
label_Volt2 = tk.Label(top, text="设置电压2(V)").grid(row=13, column=1, sticky="W")
label_Time2 = tk.Label(top, text="设置持续时间2(S)").grid(row=14, column=1, sticky="W")

# 创建循环测试相关文本框
Volt1 = tk.Entry(top)
Time1 = tk.Entry(top)
Volt2 = tk.Entry(top)
Time2 = tk.Entry(top)

Volt1.grid(row=11, column=2, sticky="W")
Time1.grid(row=12, column=2, sticky="W")
Volt2.grid(row=13, column=2, sticky="W")
Time2.grid(row=14, column=2, sticky="W")

global Circle

# 创建循环测试按钮
def btnLoopTestClicked():
    Circle = 1
    while Circle:
        time.sleep(0.1)
        sock.send(bytes(":VOLT " + Volt1.get(), encoding='utf-8'))
        time.sleep(int(Time1.get()))
        sock.send(bytes(":VOLT " + Volt2.get(), encoding='utf-8'))
        time.sleep(int(Time2.get()))


btnLoopTest = tk.Button(top, text="开始循环测试", command=btnLoopTestClicked).grid(row=15, column=1, sticky="W")

def btnLoopTestStopClicked():
    Circle = 0
    
btnLoopTestStop = tk.Button(top, text="停止循环测试", command=btnLoopTestStopClicked).grid(row=15, column=2, sticky="W")

# 运行并显示窗口
top.mainloop()

