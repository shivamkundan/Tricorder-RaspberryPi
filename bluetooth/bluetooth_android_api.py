'''!
@brief For bluetooth communication with Android devices.
@file bluetooth_android_api.py Contains code for Android bluetooth communication.
'''

# from jnius import autoclass

# class AndroidBluetoothClass:

#     def getAndroidBluetoothSocket(self,DeviceName):
#         paired_devices = self.BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
#         socket = None
#         for device in paired_devices:
#             if device.getName() == DeviceName:
#                 socket = device.createRfcommSocketToServiceRecord(
#                     self.UUID.fromString("00001101-0000-1000-8000-00805F9B34FB"))
#                 self.ReceiveData = self.BufferReader(self.InputStream(socket.getInputStream()))
#                 self.SendData = socket.getOutputStream()
#                 socket.connect()
#                 self.ConnectionEstablished = True
#                 print('Bluetooth Connection successful')
#         return self.ConnectionEstablished


#     def BluetoothSend(self, Message, *args):
#         if self.ConnectionEstablished == True:
#             self.SendData.write(Message)
#         else:
#             print('Bluetooth device not connected')


#     def BluetoothReceive(self,*args):
#         DataStream = ''
#         if self.ConnectionEstablished == True:
#             DataStream = str(self.ReceiveData.readline())
#         return DataStream


#     def __init__(self):
#         self.BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
#         self.BluetoothDevice = autoclass('android.bluetooth.BluetoothDevice')
#         self.BluetoothSocket = autoclass('android.bluetooth.BluetoothSocket')
#         self.UUID = autoclass('java.util.UUID')
#         self.BufferReader = autoclass('java.io.BufferedReader')
#         self.InputStream = autoclass('java.io.InputStreamReader')
#         self.ConnectionEstablished = False


#     def __del__(self):
#         print('class AndroidBluetooth destroyer')