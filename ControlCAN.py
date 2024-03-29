from ctypes import *


class ControlCAN:
    class TVCI_INIT_CONFIG(Structure):
        _fields_ = [('AccCode', c_uint),
                    ('AccMask', c_uint),
                    ('Reserved', c_uint),
                    ('Filter', c_ubyte),
                    ('Timing0', c_ubyte),
                    ('Timing1', c_ubyte),
                    ('Mode', c_ubyte)]

    class TVCI_BOARD_INFO(Structure):
        _fields_ = [('hw_Version', c_ushort),
                    ('fw_Version', c_ushort),
                    ('dr_Version', c_ushort),
                    ('in_Version', c_ushort),
                    ('irq_Num', c_ushort),
                    ('can_Num', c_byte),
                    ('str_Serial_Num', c_byte * 20),
                    ('str_hw_Type', c_byte * 40),
                    ('Reserved', c_ushort * 4)]

    class TVCI_ERR_INFO(Structure):
        _fields_ = [('ErrCode', c_uint),
                    ('Passive_ErrData', c_byte * 3),
                    ('ArLost_ErrData', c_byte)]

    class TVCI_CAN_STATUS(Structure):
        _fields_ = [('ErrInterrupt', c_ubyte),
                    ('regMode', c_ubyte),
                    ('regStatus', c_ubyte),
                    ('regALCapture', c_ubyte),
                    ('regECCapture', c_ubyte),
                    ('regEWLimit', c_ubyte),
                    ('regRECounter', c_ubyte),
                    ('regTECounter', c_ubyte),
                    ('Reserved', c_uint)]

    class TVCI_CAN_OBJ(Structure):
        _fields_ = [('ID', c_uint),
                    ('TimeStamp', c_uint),
                    ('TimeFlag', c_ubyte),
                    ('SendType', c_ubyte),
                    ('RemoteFlag', c_ubyte),
                    ('ExternFlag', c_ubyte),
                    ('DataLen', c_ubyte),
                    ('Data', c_ubyte * 8),
                    ('Reserved', c_ubyte * 3)]

    def __init__(self):
        self.libdll = windll.LoadLibrary('../can_tools_gather/ControlCAN.dll')
        self.libdll.VCI_OpenDevice.argtypes = [c_uint, c_uint, c_uint]
        self.libdll.VCI_OpenDevice.restype = c_uint
        self.libdll.VCI_CloseDevice.argtypes = [c_uint, c_uint]
        self.libdll.VCI_CloseDevice.restype = c_uint
        self.libdll.VCI_InitCAN.argtypes = [c_uint, c_uint, c_uint, POINTER(ControlCAN.TVCI_INIT_CONFIG)]
        self.libdll.VCI_InitCAN.restype = c_int
        self.libdll.VCI_ReadBoardInfo.argtypes = [c_uint, c_uint, POINTER(ControlCAN.TVCI_BOARD_INFO)]
        self.libdll.VCI_ReadBoardInfo.restype = c_uint
        self.libdll.VCI_ReadErrInfo.argtypes = [c_uint, c_int, c_int, POINTER(ControlCAN.TVCI_ERR_INFO)]
        self.libdll.VCI_ReadErrInfo.restype = c_uint
        self.libdll.VCI_ReadCANStatus.argtypes = [c_uint, c_int, c_int, POINTER(ControlCAN.TVCI_CAN_STATUS)]
        self.libdll.VCI_ReadCANStatus.restype = c_uint
        self.libdll.VCI_GetReference.argtypes = [c_uint, c_int, c_int, c_int, c_void_p]
        self.libdll.VCI_GetReference.restype = c_uint
        self.libdll.VCI_SetReference.argtypes = [c_uint, c_int, c_int, c_int, c_void_p]
        self.libdll.VCI_SetReference.restype = c_uint
        self.libdll.VCI_GetReceiveNum.argtypes = [c_uint, c_int, c_int]
        self.libdll.VCI_GetReceiveNum.restype = c_ulong
        self.libdll.VCI_ClearBuffer.argtypes = [c_uint, c_int, c_int]
        self.libdll.VCI_ClearBuffer.restype = c_int
        self.libdll.VCI_StartCAN.argtypes = [c_uint, c_int, c_int]
        self.libdll.VCI_StartCAN.restype = c_int
        self.libdll.VCI_ResetCAN.argtypes = [c_uint, c_int, c_int]
        self.libdll.VCI_ResetCAN.restype = c_int
        self.libdll.VCI_Transmit.argtypes = [c_uint, c_int, c_int, POINTER(ControlCAN.TVCI_CAN_OBJ), c_ulong]
        self.libdll.VCI_Transmit.restype = c_ulong
        self.libdll.VCI_Receive.argtypes = [c_uint, c_int, c_int, POINTER(ControlCAN.TVCI_CAN_OBJ), c_ulong, c_int]
        self.libdll.VCI_Receive.restype = c_ulong

    '''
    功能：打开一个设备
    参数：
        devtype: 设备型号，参加文档的2.1表格，一般用3
        devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
        reserved： 保留
    返回值：
        1-成功，0-失败
    '''

    def VCI_OpenDevice(self, devtype: c_uint, devindex: c_uint, reserved: c_uint) -> c_uint:
        ret = self.libdll.VCI_OpenDevice(devtype, devindex, reserved)
        return ret

    '''
    功能：关闭一个设备
    参数：
        devtype: 设备型号，参加文档的2.1表格，一般用3
        devindex:设备索引号，第一个卡为0，当插入第二个设备时，索引号为1
    返回值：
        1-成功，0-失败
    '''

    def VCI_CloseDevice(self, devtype: c_uint, devindex: c_uint) -> c_uint:
        ret = self.libdll.VCI_CloseDevice(devtype, devindex)
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

    def VCI_InitCAN(self, devtype: c_uint, devindex: c_uint, canindex: c_uint,
                    vci_init_config: POINTER(TVCI_INIT_CONFIG)) -> c_uint:
        ret = self.libdll.VCI_InitCAN(devtype, devindex, canindex, vci_init_config)
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

    def VCI_ReadBoardInfo(self, devtype: c_uint, devindex: c_uint, vci_board_info: POINTER(TVCI_BOARD_INFO)) -> c_uint:
        ret = self.libdll.VCI_ReadBoardInfo(devtype, devindex, vci_board_info)
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

    def VCI_ReadErrInfo(self, devtype: c_uint, devindex: c_uint, canindex: c_uint,
                        vci_err_info: POINTER(TVCI_ERR_INFO)) -> c_uint:
        ret = self.libdll.VCI_ReadErrInfo(devtype, devindex, canindex, vci_err_info)
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

    def VCI_ReadCANStatus(self, devtype: c_uint, devindex: c_uint, canindex: c_uint,
                          vci_can_status: POINTER(TVCI_CAN_STATUS)) -> c_uint:
        ret = self.libdll.VCI_ReadCANStatus(devtype, devindex, canindex, vci_can_status)
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

    def VCI_GetReference(self, devtype: c_uint, devindex: c_uint, canindex: c_uint,
                         reftype: c_uint, pdata: c_void_p) -> c_uint:
        ret = self.libdll.VCI_GetReference(devtype, devindex, canindex, reftype, pdata)
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

    def VCI_SetReference(self, devtype: c_uint, devindex: c_uint, canindex: c_uint,
                         reftype: c_uint, pdata: c_void_p) -> c_uint:
        ret = self.libdll.VCI_SetReference(devtype, devindex, canindex, reftype, pdata)
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

    def VCI_GetReceiveNum(self, devtype: c_uint, devindex: c_uint, canindex: c_uint) -> c_ulong:
        ret = self.libdll.VCI_GetReceiveNum(devtype, devindex, canindex)
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

    def VCI_ClearBuffer(self, devtype: c_uint, devindex: c_uint, canindex: c_uint) -> c_uint:
        ret = self.libdll.VCI_ClearBuffer(devtype, devindex, canindex)
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

    def VCI_StartCAN(self, devtype: c_uint, devindex: c_uint, canindex: c_uint) -> c_uint:
        ret = self.libdll.VCI_StartCAN(devtype, devindex, canindex)
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

    def VCI_ResetCAN(self, devtype: c_uint, devindex: c_uint, canindex: c_uint) -> c_uint:
        ret = self.libdll.VCI_ResetCAN(devtype, devindex, canindex)
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

    def VCI_Transmit(self, devtype: c_uint, devindex: c_uint, canindex: c_uint, vci_can_obj: POINTER(TVCI_CAN_OBJ),
                     count: c_ulong) -> c_ulong:
        ret = self.libdll.VCI_Transmit(devtype, devindex, canindex, vci_can_obj, count)
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

    def VCI_Receive(self, devtype: c_uint, devindex: c_uint, canindex: c_uint, vci_can_obj: POINTER(TVCI_CAN_OBJ),
                    count: c_ulong, waittime: c_int) -> c_ulong:
        ret = self.libdll.VCI_Receive(devtype, devindex, canindex, vci_can_obj, count, waittime)
        return ret


import time


def test():
    print('test..')
    # 创建ATCmd对象
    ctrlcan = ControlCAN()
    devtype = 3
    devidx = 0
    canidx = 0
    # 打开设备
    if ctrlcan.VCI_OpenDevice(devtype, devidx, 0) == 1:
        initconfig = ctrlcan.TVCI_INIT_CONFIG()
        initconfig.AccCode = 0
        initconfig.AccMask = 0xFFFFFFFF
        initconfig.Reserved = 0
        initconfig.Filter = 0
        # 以下两个值需要查表
        initconfig.Timing0 = 0x01
        initconfig.Timing1 = 0x1C
        initconfig.Mode = 0

        if ctrlcan.VCI_InitCAN(devtype, devidx, canidx, initconfig) == 1:
            if ctrlcan.VCI_StartCAN(devtype, devidx, canidx) == 1:
                while (1):
                    vci_can_obj = ctrlcan.TVCI_CAN_OBJ()
                    vci_can_obj.ID = 100  # 帧 ID
                    vci_can_obj.ExternFlag = 1  # 扩展帧
                    # 发送数据
                    success_num = ctrlcan.VCI_Transmit(devtype, devidx, canidx, vci_can_obj, 1)
                    print('发送帧 ID为：%d,发送成功帧数为：%d' % (vci_can_obj.ID, success_num))
                    # 接收数据
                    recvcount = ctrlcan.VCI_Receive(devtype, devidx, canidx, vci_can_obj, 1, 200)
                    if recvcount > 0:
                        print('接收帧 ID为: %d,接收时间戳为：%d' % (vci_can_obj.ID, vci_can_obj.TimeStamp))
                    time.sleep(1)
            else:
                print('VCI_StartCAN failed')
        else:
            print('VCI_InitCAN failed')
    else:
        print('VCI_OpenDevice failed')
    # 释放

    # 删除
    del ctrlcan


if __name__ == '__main__':
    test()
