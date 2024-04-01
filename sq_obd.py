import ControlCAN_lib
import time
import datetime
import threading
import json
import sys

class Tee:
    def __init__(self, filename):
        self.filename = filename

    def write(self, string):
        if not isinstance(string, Tee):
            with open(self.filename, 'a') as f:
                f.write(string)
            sys.__stdout__.write(string)
            
    def flush(self):
        pass

def print_to_tee(*args, **kwargs):
    string = " ".join(map(str, args)) + " " + str(kwargs.get("end", ""))
    sys.stdout.write(string)
    sys.stdout.flush() 
    with open("output.txt", 'a') as f:
        f.write(string)
    

print("----------------------陕汽OBD测试工具-----------------------------")
class CAN:
    def __init__(self, filename):
        self.can_obj = ControlCAN_lib.control_can()
        self.rev = self.can_obj.TVCI_CAN_OBJ()
        self.initialized = False

        self.recv_thread = None
        self.send_thread = None
        self.stop_event = threading.Event()
        self.FileName = filename
        if filename == "syc_7e0.json":
            self.target_id = 0x000007E0
        else:
            self.target_id = 0x18da00f1
            
        self.jsondata = None
        self.data_map = {
            "Condition":[],
            "MIL_F491":[], 
            "MIL":[], 
            "VIN":[], 
            "CALID":[], 
            "CVN":[], 
            "IUPR":[], 
            "IUPR_F808":[],
            "FAULTCODE":[]
            }
        
    def initialize(self, baud_rate):
        init_obj = ControlCAN_lib.create_init_config(self.can_obj, baud_rate)
        if ControlCAN_lib.vci_open_device(self.can_obj, 3, 0, 0) == 0:
            print("Open Can Device Fail.")
            return False
        else:
            print("Open Can Device Success.")
        if ControlCAN_lib.vci_init_can(self.can_obj, 3, 0, 0, init_obj) == 0:
            print("Init Can Device Fail.")
            return False
        else:
            print("Init Can Device Success.")
        if ControlCAN_lib.vci_start_can(self.can_obj, 3, 0, 0) == 0:
            print("Start Can Device Fail.")
            return False
        else:
            print("Start Can Device Success.")
        if ControlCAN_lib.vci_clear_buffer(self.can_obj, 3, 0, 0) == 0:
            print("Clear Can Device Cache Fail.")
            return False
        else:
            print("Clear Can Device Cache Success.")
        self.initialized = True
        return True
    
    def close(self):
        if self.initialized:
            if ControlCAN_lib.vci_clear_buffer(self.can_obj, 3, 0, 0) == 0:
                print("Clear Can Device Fail.")
                return False
            else:
                print("Clear Can Device Success.")
            if ControlCAN_lib.vci_close_device(self.can_obj, 3, 0) == 0:
                print("Close Can Device Fail.")
                return False
            else:
                print("Close Can Device Success.")
            self.initialize = False
            return
        
    def loadJsonFile(self):
        try:
            with open(self.FileName, "r") as f:
                self.jsondata = json.load(f)
        except Exception as e:
            print(f"Read Json File Fail: {e}")
    
    def ParseElementInfo(self):
        if self.jsondata is not None:
            for key in self.data_map:
                element_info = self.jsondata.get(key)
                if element_info is not None and "Count" in element_info and "Info" in element_info:
                    if element_info["Count"] <= len(element_info["Info"]):
                        self.data_map[key] = element_info["Info"]
                    else:
                        print(f"{key} Count is less than Info length.")
                else:
                    print(f"Invalid or missing 'Info' list for {key} in Json data.")


    def create_send_can(self, can_id, can_data):
        datas = ''.join(can_data.split())
        can = ControlCAN_lib.create_vci_obj(self.can_obj, int(can_id, 16), 1, 8, datas)
        return can
    
    def send_can(self, obj):
        try:
            ControlCAN_lib.vci_transmit(self.can_obj, 3, 0, 0, obj, 1)
        except Exception as e:
            print(f"Error sending CAN message: {e}")

    def start(self):
        if self.recv_thread is None:
            self.recv_thread = threading.Thread(target=self.recvCan)
            self.recv_thread.start()

        if self.send_thread is None:
            self.send_thread = threading.Thread(target=self.sendCan)
            self.send_thread.start()
    
    def stop(self):
        self.stop_event.set()
        if self.recv_thread.is_alive():
            self.recv_thread.join()
        if self.send_thread.is_alive():
            self.send_thread.join()
        self.close()

    def recvCan(self):
        while not self.stop_event.is_set():
            res = ControlCAN_lib.vci_receive(self.can_obj, 3, 0, 0, self.rev, 1, 2000)
            if res == 1:
                Data = self.rev.Data
                Id = self.rev.ID
                dt_ms = datetime.datetime.now().strftime('%H:%M:%S:%f')
                if Id == 0x18da00f1 or Id == 0x000007E0:
                    print(dt_ms, 'recv id={:02X} '.format(Id), end="")
                    print('data=', end='')
                    for i in Data:
                        print('{:02X} '.format(i), end='')
                    print('')
                if Id == self.target_id:
                    if Data[2] == 0xF4 and Data[3] == 0x91:
                        send_data = self.data_map["MIL_F491"]
                        for info in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)

                    if Data[2] == 0xF4 and Data[3] == 0x01:
                        send_data = self.data_map["MIL"]
                        for info in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)

                    if Data[2] == 0xF8 and Data[3] == 0x02:
                        send_data = self.data_map["VIN"]
                        for info in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)

                    if Data[2] == 0xF8 and Data[3] == 0x04:
                        send_data = self.data_map["CALID"]
                        for info in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)

                    if Data[2] == 0xF8 and Data[3] == 0x06:
                        send_data = self.data_map["CVN"]
                        for into in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)

                    if Data[2] == 0xF8 and Data[3] == 0x0B:
                        send_data = self.data_map["IUPR"]
                        for info in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)

                    if Data[2] == 0xF8 and Data[3] == 0x08:
                        send_data = self.data_map["IUPR_F808"]
                        for info in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)

                    if Data[0] == 0x05 and Data[1] == 0x19 and Data[2] == 0x42 and Data[3] == 0x33:
                        send_data = self.data_map["FAULTCODE"]
                        for info in send_data:
                            can_info = self.create_send_can(info["id"], info["data"])
                            self.send_can(can_info)
                            time.sleep(0.05)



    def sendCan(self):
        while not self.stop_event.is_set():
            try:
                send_data = self.data_map["Condition"]
                for info in send_data:
                    can_info = self.create_send_can(info["id"], info["data"])
                    self.send_can(can_info)
                    time.sleep(0.5)
            except (KeyError, TypeError, IndexError) as e:
                print(f"Error sending CAN message: {e}")
            except Exception as e:
                print(f"An unexpected error occurrd: {e}")

    def putstoFile(self):
        try:
           sys.stdout = Tee('output.txt')
        except IOError as e:
            print(f"Error opening file for writing: {e}")

if __name__ == '__main__':
    print("请选择：\r\n 1.商用车德尔福(syc_7e0.json) \r\n 2.商用车(syc.json) \r\n 3.陕重汽HD(sq_hd.json) \r\n 4.陕重汽X3000(sq_x3000.json) \r\n")
    protocol = int(input("请输入选择"))
    filename = ""
    if protocol == 1:
        filename = "syc_7e0.json"
    if protocol == 2:
        filename = "syc.json"
    if protocol == 3:
        filename = "sq_hd.json"
    if protocol == 4:
        filename = "sq_x3000.json"
    can = CAN(filename)
    bard_rate = int(input("请输入波特率(1-250K, 0-500K)"))
    can.putstoFile()
    can.loadJsonFile()
    can.ParseElementInfo()
    if can.initialize(bard_rate):
        can.start()
        input("Please input Enter quit.\r\n")
        can.stop()
    else:
        print("Can Device Initialize Fail, Unable To Proceed.")

