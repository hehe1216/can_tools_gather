import json

class ObdInfo:
    def __init__(self):
        self.FileName = "obd_config.json"
        self.jsondata = ""

    def loadJsonFile(self):
        try:
            with open(self.FileName, "r") as f:
                self.jsondata = json.load(f)
        except:
            print("读取json文件失败!")
        return self.jsondata

    def IsSrcAddrAdapter(self):
        SrcAddrAdapter = self.jsondata["SrcAddrAdapter"]
        return SrcAddrAdapter
    
    def IsProtocolAdapter(self):
        ProtocolAdapter = self.jsondata["ProtocolAdapter"] 
        return ProtocolAdapter

    def GetCondition(self):
        condition = self.jsondata["Condition"]
        condition_count = condition["Count"]
        condition_info = condition["Info"]
        return condition_count, condition_info
    
    def GetMil(self):
        mil = self.jsondata["MIL"]
        mil_count = mil["Count"]
        mil_info = mil["Info"]
        return mil_count, mil_info

    def GetVin(self):
        vin = self.jsondata["VIN"]
        vin_count = vin["Count"]
        vin_info = vin["Info"]
        return vin_count, vin_info

    def GetCalid(self):
        calid = self.jsondata["CALID"]
        calid_count = calid["Count"]
        calid_info = calid["Info"]
        return calid_count, calid_info

    def GetCvn(self):
        cvn = self.jsondata["CVN"]
        cvn_count = cvn["Count"]
        cvn_info = cvn["Info"]
        return cvn_count, cvn_info

    def GetIupr(self):
        iupr = self.jsondata["IUPR"]
        iupr_count = iupr["Count"]
        iupr_info = iupr["Info"]
        return iupr_count, iupr_info

    def GetFaultCode(self):
        fault_code = self.jsondata["FAULTCODE"]
        fault_code_count = fault_code["Count"]
        fault_code_info = fault_code["Info"]
        return fault_code_count,fault_code_info


if __name__ == '__main__':
    obd = ObdInfo()
    jsondata = obd.loadJsonFile()
    print(obd.IsSrcAddrAdapter())
    print(obd.IsProtocolAdapter())

    condition_count, condition_info = obd.GetCondition()
    print(condition_count)
    print(condition_info)

    mil_count, mil_info = obd.GetMil()
    print(mil_count)
    print(mil_info)

    vin_count, vin_info = obd.GetVin()
    print(vin_count)
    print(vin_info)

    calid_count, calid_info = obd.GetCalid()
    print(calid_count)
    print(calid_info)

    cvn_count, cvn_info = obd.GetCvn()
    print(cvn_count)
    print(cvn_info)

    iupr_count, iupr_info = obd.GetIupr()
    print(iupr_count)
    print(iupr_info)

    fault_code_count, fault_code_info = obd.GetFaultCode()
    print(fault_code_count)
    print(fault_code_info)