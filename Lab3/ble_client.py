# rpi ble controlling notification (discription CCCD)
# ble_scan_connect.py:
from bluepy.btle import Peripheral, UUID
from bluepy.btle import Scanner, DefaultDelegate
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print ("Discovered device", dev.addr)
        elif isNewData:
            print ("Received new data from", dev.addr)
scanner = Scanner().withDelegate(ScanDelegate())
devices = scanner.scan(10.0)
n=0
addr = []
print ("====================================================")
for dev in devices:

    for (adtype, desc, value) in dev.getScanData():
        print (" %s = %s" % (desc, value))
        if desc == "Complete Local Name": #<Note> 讓它顯示Device name
            name = value
    name = None
    if name:
        print(" Device Name: %s" % name)
    else:
        print(" Device Name: N/A")
    print ("%d: Device %s (%s), RSSI=%d dB" % (n, dev.addr, dev.addrType, dev.rssi))
    addr.append(dev.addr)
    n += 1
    
    
    
    
    
    print ("====================================================")


number = input('Enter your device number: ')
print ('Device', number)
num = int(number)
print (addr[num])
#
print ("Connecting...")
dev = Peripheral(addr[num], 'random')
#
print ("Services...")
for svc in dev.services:
    print (str(svc))
#
try:
    testService = dev.getServiceByUUID(UUID(0xfff0))
    # BDB56B1F-BC66-4723-A4AB-E08CA3431E13
    # testService = dev.getServiceByUUID(UUID('BDB56B1F-BC66-4723-A4AB-E08CA3431E13'))
    for ch in testService.getCharacteristics():
        print (str(ch))
    #
    ch = dev.getCharacteristics(uuid=UUID(0xfff4))[0]
    # Locate the characteristic you want to interact with
    print("ok1")
    # ch = dev.getCharacteristics(uuid=UUID('9381B14A-9B99-4969-A39E-C6A40E8CB0E0'))[0]
    if (ch.supportsRead()):
        print("ok2")
        print (ch.read())
        print("ok3")
    print("ch.valHandle",ch.valHandle)
    # p = btle.Peripheral(<MAC ADDRESS>, btle.ADDR_TYPE_RANDOM)
    # ================
    # dev.writeCharacteristic(ch.valHandle+1, b"\x02\x00")
    # 2902
    # discriptor = ch.getDescriptors(uuid=UUID(0x2902))
    # while True:
    #     if dev.waitForNotifications(1.0):
    #         # handleNotification() was called
    #         ch2 = dev.getCharacteristics(uuid=UUID(0xfff1))[0]
    #         if (ch.supportsRead()):
    #             # print("ok2")
    #             print (ch.read())
    #         continue

    #     print("Waiting...")

    # 找到 CCCD 描述子
    
    descriptor = ch.getDescriptors()
    for d in descriptor:
        print(f"Descriptor UUID: {d.uuid}, handle: {d.handle}")
    descriptor2 = ch.getDescriptors(forUUID=UUID(0x2902))[0]
    # 寫入 0x0100 以開啟 notification
    dev.writeCharacteristic(descriptor2.handle, b"\x01\x00", withResponse=True)
    # 通知處理迴圈
    while True:
        if dev.waitForNotifications(1.0):
            # handleNotification() 被觸發
            print(ch.read())
            continue

        # # 如果 characteristic 支援 read
        # if ch.supportsRead():
        #     print(ch.read())
        # # ===============
    # # Now let's handle the CCCD for this characteristic
    # # This assumes the characteristic supports notifications/indications
    # # for desc in ch.descriptors:
    # if ch.getDescriptors() is not None: 
    #     print ("desc is not none")
    # else: 
    #     print ("desc is none")
    # for desc in ch.getDescriptors():
    #     print(f"Descriptor {desc.uuid}: {desc.read()}")
        
    #     # If this descriptor is a CCCD, we can write to it to enable notifications/indications
    #     if desc.uuid == UUID(0x2902):  # CCCD descriptor UUID
    #         print("Writing to CCCD to enable notifications or indications.")
    #         desc.write(bytes([0x00, 0x02]))  # Write 0x0002 to enable indications
            
    #         print("CCCD written successfully.")
    #         break
    #
finally:
    dev.disconnect() 
