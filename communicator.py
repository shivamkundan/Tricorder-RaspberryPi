#!/usr/bin/python3
from bluetooth import *
from dataclasses import dataclass

# ----- my libs ----- #
from paths_and_utils import *

# Bluetooth
uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
addr='B8:27:EB:E7:92:9C' #bluetooth address of sensor server

# For direct serial connection
USB_SERIAL_PORT='/dev/ttyACM0'


class Communicator():
	def __init__(self):
		self.connected=False
		self.sock=None
		self.comm_count=0
		self.connect=None
		self.send_and_recv=None

class SerialUSBManager(Communicator):
	def __init__(self):
		super().__init__()

	def connect_serial(self,port=USB_SERIAL_PORT):
		import serial
		ser = serial.Serial(
			port=port, # Change this according to connection methods, e.g. /dev/ttyUSB0
			baudrate = 115200,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS,
			timeout=1
		)

	def get_serial_vals(self,msg,dict_names_list):
		# ==========================================
		ser.write(msg.encode('utf-8'))

		curr_line=(ser.readline()).decode('utf-8')


		if curr_line=='':
			return {}
		if curr_line[0]=='*':
			return {}
		# print(curr_line)

		ser.write(msg.encode('utf-8'))
		x={}

		curr_line=(ser.readline()).decode('utf-8').lstrip(' ').rstrip('\r\n')
		# print (curr_line)

		for item,name in zip(curr_line.split(' '),dict_names_list):
			try:
				val=item.split(":")[1]
			except IndexError:
				val=-1
			# print (val)
			x[name]=val
		print (msg,":",x)
		return x

		# ==========================================

class BluetoothManager(Communicator):
	def __init__(self):
		super().__init__()
		self.connect=self.connect_bluetooth
		self.send_and_recv=self.get_bluetooth_vals
		self.replace_chars=[' ','{','}','*',"'",'\x00']

	def connect_bluetooth(self):

		print ('finding service...')


		print("Searching for SampleServer on %s" % addr)

		# search for the SampleServer service

		connected=False
		while connected==False:
			try:
				service_matches=''
				service_matches = find_service( uuid = uuid, address = addr )

				if len(service_matches) != 0:
					first_match = service_matches[0]
					port = first_match["port"]
					name = first_match["name"]
					host = first_match["host"]
					# Create the client socket
					print("Waiting for connection on RFCOMM channel %d" % port)
					sock=BluetoothSocket( RFCOMM )
					sock.connect((host, port))
					connected=True
			except btcommon.BluetoothError as error:
					print( "Caught BluetoothError: ", error)
					time.sleep(2)
		pygame.event.post(BLUETOOTH_CONNECTED)
		print("connected.  type stuff")
		self.client_sock=sock
		# return sock


	def get_bluetooth_vals(self,msg):
		try:

			# print (self.bluetooth_count)
			# print('sending: ',msg)
			if len(msg)<MAX_BYTES:
				msg=msg.rstrip(' ')
				for kk in range(len(msg),MAX_BYTES):
					msg+='*'
			# print('msg len: ',len(msg))
			self.client_sock.send(msg)
			self.recv_data = self.client_sock.recv(MAX_BYTES).decode("utf-8")

			for char in self.replace_chars:
				self.recv_data=self.recv_data.replace(char,'')

			splitup=self.recv_data.split(',')

			for item1 in splitup:
				# print (item1)
				z=item1.strip().split(':')
				k,v=z[0],z[1]
				self.sensor_dict[k]=v
			self.bluetooth_count+=1
			# print()
			return self.sensor_dict

		except IndexError:
			return SENSOR_DICT
		except btcommon.BluetoothError:
			pygame.event.post(BLUETOOTH_DISCONNECTED)
		except Exception as e:
			# print ('err: get_bluetooth_vals')
			raise(e)

if __name__ == '__main__':
	B=BluetoothManager()
	B.connect()