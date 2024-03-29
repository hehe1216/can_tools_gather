import ControlCAN_lib
import time
import datetime

can_obj = ControlCAN_lib.control_can()
rev = can_obj.TVCI_CAN_OBJ()
print("---------------------陕汽商用车锁车工具-------------------------")
bard = input("请输入波特率(1.250K  0.500K)")
init_obj = ControlCAN_lib.create_init_config(can_obj, int(bard))
print("打开设备%d" % (ControlCAN_lib.vci_open_device(can_obj, 3, 0, 0)))
print("初始化%d" % (ControlCAN_lib.vci_init_can(can_obj, 3, 0, 0, init_obj)))
print("启动%d" % (ControlCAN_lib.vci_start_can(can_obj, 3, 0, 0)))
print("清空缓存区%d" % (ControlCAN_lib.vci_clear_buffer(can_obj, 3, 0, 0)))
time.sleep(1)

g_passcode_cnt = 0


def create_send_can(can_id, can_data):
    lists = can_data.split()
    datas = ''
    for cell in lists:
        datas += cell
    can = ControlCAN_lib.create_vci_obj(can_obj, can_id, 1, 8, datas)
    return can

def send_can(obj):
    ControlCAN_lib.vci_transmit(can_obj, 3, 0, 0, obj, 1)

def run():
    while True:
        res = ControlCAN_lib.vci_receive(can_obj, 3, 0, 0, rev, 1, 2000)
        if res == 1:
            Data = rev.Data
            Id = rev.ID
            dt_ms = datetime.datetime.now().strftime('%H:%M:%S:%f')
            if Id == 0x18FFD4FD or Id == 0x18FFD6FD or Id == 0x18FF10A5 or Id == 0x18FF11A5 or Id == 0x18FF12A5:
                print(dt_ms, 'recv id={:02X} '.format(Id), end="")
                print('data=', end='')
                for i in Data:
                    print('{:02X} '.format(i), end='')
                print('')

            # 激活
            if Id == 0x18FFD4FD and Data[0] == 0x0E and Data[1] == 0xCA:
                data1 = create_send_can(0x18FF0800, "00 00 09 00 FF FF FF FF")
                send_can(data1)

            # 关闭激活
            if Id == 0x18FFD4FD and Data[0] == 0x47 and Data[1] == 0x87:
                data2 = create_send_can(0x18FF0800, "00 00 08 00 FF FF FF FF")
                send_can(data2)

            # 锁车
            if Id == 0x18FFD6FD and Data[0] == 0x00 and Data[1] == 0x00:
                data3 = create_send_can(0x18FF0800, "00 00 0F 00 00 00 00 00")
                send_can(data3)

            # 解锁
            if Id == 0x18FFD6FD and Data[0] == 0x60 and Data[1] == 0x6D:
                data4 = create_send_can(0x18FF0800, "00 00 0D 00 FF FF FF FF")
                send_can(data4)

            # 密码解锁
            if Id == 0x18FF11A5:
                global g_passcode_cnt
                g_passcode_cnt = g_passcode_cnt + 1
                if g_passcode_cnt == 10:
                    isinput = input("是否输入密码:(Y/N)")
                    if isinput == 'Y' or isinput == 'y':
                        candata = input("请输入密码:(格式:01 02 03 04 05 06 00 00)")
                        data5 = create_send_can(0x18FF6517, candata)
                        send_can(data5)
                    g_passcode_cnt = 0

            # 密码校验结果
            if Id == 0x18FF12A5:
                if Data[0] == 0:
                    print("密码正确！")
                if Data[0] == 1:
                    print("密码错误！")  
                    isinput = input("是否输入密码:(Y/N)")
                    if isinput == 'Y' or isinput == 'y':
                        candata = input("请输入密码:(格式:01 02 03 04 05 06 00 00)")
                        data6 = create_send_can(0x18FF6517, candata)
                        send_can(data6)  

            # 锁车状态--发给仪表                
            if Id == 0x18FF10A5:
                if Data[0] == 0:
                    print("未锁车！")
                if Data[0] == 1:
                    print("主动锁车！")
                if Data[0] == 2:
                    print("被动锁车")
while True:
    try:
        run()
    
    except KeyboardInterrupt:
        print("关闭设备%d" % (ControlCAN_lib.vci_close_device(can_obj, 3, 0)))
        exit()