import ctypes
from _ctypes import POINTER
import ControlCAN
from ControlCAN import *
import re
import datetime
import time

'''
创建对象
'''


def control_can():
    return ControlCAN()


'''
功能：打开一个设备
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    reserved： 保留
返回值：
    1-成功，0-失败
'''


def vci_open_device(control_can_obj, devtype, devindex, reserved):
    ret = control_can_obj.VCI_OpenDevice(devtype, devindex, reserved)
    return ret


'''
功能：关闭一个设备
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
返回值：
    1-成功，0-失败
'''


def vci_close_device(control_can_obj, devtype, devindex):
    ret = control_can_obj.VCI_CloseDevice(devtype, devindex)
    return ret


'''
功能：初始化CAN通道
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
    vci_init_config: 初始化配置
返回值：
    1-成功，0-失败
'''


def vci_init_can(control_can_obj, devtype, devindex, canindex,
                 vci_init_config: POINTER(ControlCAN.TVCI_INIT_CONFIG)):
    ret = control_can_obj.VCI_InitCAN(devtype, devindex, canindex, vci_init_config)
    return ret


'''
功能：读取板信息
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    vci_board_info：板信息
返回值：
    1-成功，0-失败
'''


def vci_read_board_info(control_can_obj, devtype, devindex,
                        vci_board_info: POINTER(ControlCAN.TVCI_BOARD_INFO)):
    ret = control_can_obj.VCI_ReadBoardInfo(devtype, devindex, vci_board_info)
    return ret


'''
功能：读取错误信息
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
    vci_err_info: 错误信息结构
返回值：
    1-成功，0-失败
'''


def vci_read_err_info(control_can_obj, devtype, devindex, canindex,
                      vci_err_info: POINTER(ControlCAN.TVCI_ERR_INFO)):
    ret = control_can_obj.VCI_ReadErrInfo(devtype, devindex, canindex, vci_err_info)
    return ret


'''
功能：读取CAN状态
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
    vci_can_status: can status信息结构
返回值：
    1-成功，0-失败
'''


def vci_read_can_status(control_can_obj, devtype, devindex, canindex,
                        vci_can_status: POINTER(ControlCAN.TVCI_CAN_STATUS)):
    ret = control_can_obj.VCI_ReadCANStatus(devtype, devindex, canindex, vci_can_status)
    return ret


'''
功能：读取设备参数
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
    reftype: 参数类型
    pdata: 数据缓存区首地址
返回值：
    1-成功，0-失败
'''


def vci_get_reference(control_can_obj, devtype, devindex, canindex,
                      reftype, pdata):
    ret = control_can_obj.VCI_GetReference(devtype, devindex, canindex, reftype, pdata)
    return ret


'''
功能：设置设备参数
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
    reftype: 参数类型
    pdata: 数据缓存区首地址
返回值：
    1-成功，0-失败
'''


def vci_set_reference(control_can_obj, devtype, devindex, canindex,
                      reftype, pdata):
    ret = control_can_obj.VCI_SetReference(devtype, devindex, canindex, reftype, pdata)
    return ret


'''
功能：接收尚未读取的帧数量
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
返回值：
    返回尚未读取的帧数量
'''


def vci_get_receive_num(control_can_obj, devtype, devindex, canindex):
    ret = control_can_obj.VCI_GetReceiveNum(devtype, devindex, canindex)
    return ret


'''
功能：清空接收缓存区
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
返回值：
    1-成功，0-失败
'''


def vci_clear_buffer(control_can_obj, devtype, devindex, canindex):
    ret = control_can_obj.VCI_ClearBuffer(devtype, devindex, canindex)
    return ret


'''
功能：启动一路CAN
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
返回值：
    1-成功，0-失败
'''


def vci_start_can(control_can_obj, devtype, devindex, canindex):
    ret = control_can_obj.VCI_StartCAN(devtype, devindex, canindex)
    return ret


'''
功能：reset一路CAN
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
返回值：
    1-成功，0-失败
'''


def vci_reset_can(control_can_obj, devtype, devindex, canindex):
    ret = control_can_obj.VCI_ResetCAN(devtype, devindex, canindex)
    return ret


'''
功能：向一路CAN上发送数据
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
    VCI_CAN_OBJ: 要发送数据的数组首地址
    count： 发送帧数
返回值：
    发送成功的帧数
'''


def vci_transmit(control_can_obj, devtype, devindex, canindex, vci_can_obj, count):
    ret = control_can_obj.VCI_Transmit(devtype, devindex, canindex, vci_can_obj, count)
    sec = time.time()
    dt_ms = datetime.datetime.now().strftime('%H:%M:%S:%f')  # 含微秒的日期时间，来源 比特量化
    print(dt_ms, "send: id={:08X} ".format(vci_can_obj.ID), end="")
    print("data=", end="")
    for i in vci_can_obj.Data:
        print("{:02X} ".format(i), end="")
    print("")
    return ret


'''
功能：向一路CAN上接收数据
参数：
    devtype: 设备型号，参加文档的2.1表格，一般用3
    devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    canindex: 当前使用第几路can，0,1
    VCI_CAN_OBJ: 要发送数据的数组首地址
    count： 本次接收的数组最大长度
    waittime: 如果缓存区无数据，则等待的毫秒数，-1表示一直等待
返回值：
    1-成功，0-失败
'''


def vci_receive(control_can_obj, devtype, devindex, canindex,
                vci_can_obj,
                count, waittime):
    ret = control_can_obj.VCI_Receive(devtype, devindex, canindex, vci_can_obj, count, waittime)
    return ret


"""
处理16进制的文本
"""


def str2hex(s):
    odata = 0;
    su = s.upper()
    for c in su:
        tmp = ord(c)
        if tmp <= ord('9'):
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata


"""
创建并返回一个TVCI_CAN_OBJ结构体对象
"""


def create_vci_obj(control_can_obj, canid: int, frame_format: int, data_len: int, data: str):
    vci_can_obj = control_can_obj.TVCI_CAN_OBJ()

    vci_can_obj.ID = canid
    vci_can_obj.SendType = 0  # 正常发送
    vci_can_obj.RemoteFlag = 0  # 数据帧
    vci_can_obj.ExternFlag = frame_format  # 扩展帧
    vci_can_obj.DataLen = data_len  # 数据长度为8个字节
    # print(vci_can_obj.ExternFlag, vci_can_obj.DataLen)
    data_list = re.findall('..', data)  # 对data进行切割，每2位切割一次
    data1 = (ctypes.c_ubyte * 8)(
        *[ctypes.c_ubyte(str2hex(s)) for s in data_list[:8]])  # 将切割后的16进数据制转换成10进制数组，再将数组中每一个元素转为c_byte8类型
    vci_can_obj.Data = data1
    return vci_can_obj


def create_init_config(create_can, baud_rate=0x1):
    """
    创建并返回一个TVCI_INIT_CONFIG结构体对象
    baud_rate: 1:250k 0:500k
    """
    initconfig = create_can.TVCI_INIT_CONFIG()
    initconfig.AccCode = 0
    initconfig.AccMask = 0xFFFFFFFF
    initconfig.Reserved = 0
    initconfig.Filter = 0
    # 以下两个值需要查表
    initconfig.Timing0 = baud_rate  # 波特率 1:250K，0:500K
    initconfig.Timing1 = 0x1C
    initconfig.Mode = 0
    return initconfig


def test1():
    print('test..')
    # 创建can收发器对象
    create_can = control_can()
    print(create_can)
    devtype = 3
    devidx = 0
    canidx = 0
    count = 50
    # 打开设备
    if vci_open_device(create_can, devtype, devidx, 0) == 1:

        initconfig = ControlCAN.TVCI_INIT_CONFIG()
        initconfig.AccCode = 0
        initconfig.AccMask = 0xFFFFFFFF
        initconfig.Reserved = 0
        initconfig.Filter = 0
        # 以下两个值需要查表
        initconfig.Timing0 = 0x01  # 波特率 1:250K，0:500K
        initconfig.Timing1 = 0x1C
        initconfig.Mode = 0

        if vci_init_can(create_can, devtype, devidx, canidx, initconfig) == 1:
            if vci_start_can(create_can, devtype, devidx, canidx) == 1:
                while (1):
                    # vci_can_obj = ctrlcan.TVCI_CAN_OBJ()
                    vci_can_obj = create_vci_obj(create_can, 0x0CF00400, 1, 8, '0000006400000000')
                    print(vci_can_obj)
                    print(vci_can_obj.Data)
                    # vci_can_obj.ExternFlag = 1  # 扩展帧
                    # 发送数据
                    success_num = vci_transmit(create_can, devtype, devidx, canidx, vci_can_obj, count)
                    print('发送帧 ID为：%s,发送成功帧数为：%s' % (vci_can_obj.ID, vci_can_obj.Data))
                    # 接收数据
                    recv_count = vci_receive(create_can, devtype, devidx, canidx, vci_can_obj, 1, 200)
                    if recv_count > 0:
                        print('接收帧 ID为: %s,接收数据为：%s' % (vci_can_obj.ID, vci_can_obj.Data))
                    time.sleep(1)
            else:
                print('VCI_StartCAN failed')
        else:
            print('VCI_InitCAN failed')
    else:
        print('VCI_OpenDevice failed')
    # 释放

    # 删除
    del create_can


def hprint():
    print("hehe")


if __name__ == '__main__':
    test1()
