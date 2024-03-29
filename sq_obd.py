import ControlCAN_lib
import time
import datetime
import threading
import json

print("----------------------陕汽OBD测试工具-----------------------------")
can_obj = ControlCAN_lib.control_can()
rev = can_obj.TVCI_CAN_OBJ()
bard_rate = input("请输入波特率(1-250K, 0-500K)")
init_obj = ControlCAN_lib.create_init_config(can_obj, int(bard_rate))
print("打开设备%d" % (ControlCAN_lib.vci_open_device(can_obj, 3, 0, 0)))
print("初始化%d" % (ControlCAN_lib.vci_init_can(can_obj, 3, 0, 0, init_obj)))
print("启动%d" % (ControlCAN_lib.vci_start_can(can_obj, 3, 0, 0)))
print("清空缓存区%d" % (ControlCAN_lib.vci_clear_buffer(can_obj, 3, 0, 0)))
time.sleep(1)

class CAN:
    def __init__(self):
        self.recv_thread = None
        self.send_thread = None
        self.FileName = "obd_config.json"
        self.jsondata = ""
        self.datalist = ["SrcAddrAdapter", "ProtocolAdapter", "Condition", "MIL", "VIN", "CALID", "CVN", "IUPR", "FAULTCODE"]
        self.srcaddradapter = list()
        self.protocoladapter = list()
        self.condition = list()
        self.mil = list()
        self.vin = list()
        self.calid = list()
        self.cvn = list()
        self.iupr = list()
        self.faultcode = list()
    
    def loadJsonFile(self):
        try:
            with open(self.FileName, "r") as f:
                self.jsondata = json.load(f)
        except Exception as e:
            print(f"Read Json File Fail: {e}")

    def GetElementInfo(self, key:str):
        if key in self.datalist:
            return self.jsondata[key]
        else:
            print(f"Element {key} not found in Json data.")
            return None
    
    def ParseElementInfo(self):
        for element in can.datalist:
            if element is not None:
                element_info = self.GetElementInfo(element)
                if element_info and "Count" in element_info and "Info" in element_info:
                    count = element_info["Count"]
                    info_list = element_info["Info"]
                    if count <= len(info_list):
                        for i in range(count):
                            msg = info_list[i]
                            if element == "SrcAddrAdapter":
                                self.srcaddradapter.append(msg)
                            if element == "ProtocolAdapter":
                                self.protocoladapter.append(msg)
                            if element == "Condition":
                                self.condition.append(msg)
                            if element == "MIL":
                                self.mil.append(msg)
                            if element == "VIN":
                                self.vin.append(msg)
                            if element == "CALID":
                                self.calid.append(msg)
                            if element == "CVN":
                                self.cvn.append(msg)
                            if element == "IUPR":
                                self.iupr.append(msg)
                            if element == "FAULTCODE":
                                self.faultcode.append(msg)
                    else:
                        print("Count is less than Info length.")
                else:
                    print("Invalid or missing 'Info' list in Json data.")
            else:
                print("Invalid element.")

    def create_send_can(self, can_id, can_data):
        datas = ''.join(can_data.split())
        can = ControlCAN_lib.create_vci_obj(can_obj, can_id, 1, 8, datas)
        return can
    
    def send_can(self, obj):
        try:
            ControlCAN_lib.vci_transmit(can_obj, 3, 0, 0, obj, 1)
        except Exception as e:
            print(f"Error sending CAN message: {e}")

    def start(self):
        self.recv_thread = threading.Thread(target=self.recvCan)
        self.send_thread = threading.Thread(target=self.sendCan)
        self.recv_thread.start()
        self.send_thread.start()
    
    def recvCan(self):
        pass

    def sendCan(self):
        pass


if __name__ == '__main__':
    can = CAN()
    can.loadJsonFile()
    can.ParseElementInfo()
    print(can.srcaddradapter)
    print(can.protocoladapter)
    print(can.condition)
    print(can.mil)
    print(can.vin)
    print(can.calid)
    print(can.cvn)
    print(can.iupr)
    print(can.faultcode)
