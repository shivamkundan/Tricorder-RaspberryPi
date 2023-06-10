'''! @brief Object detection using cv2/tflite.
@file object_detection_page.py Contains defintion for ObjectDetectionPage class.
@bug Page keeps crashing. Need to restart raspberry pi to fix.
'''

from page_templates import PageTemplate
from fonts import FONT_FEDERATION
from colors import ORANGE, DARK_YELLOW

import os
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import utils
import time
import sys


class ObjectDetectionPage(PageTemplate):
	'''! Object detection using cv2/tflite'''
	def __init__(self,name):
		'''! Contstructor'''
		super().__init__(name)
		self.prev_page_name='menu_home_page'

		model="/home/pi/Sensor_Scripts/pygame_code/tricorder/sensor_pages/efficientdet_lite0.tflite"
		camera_id=0
		num_threads=4
		enable_edgetpu=False
		# Variables to calculate FPS
		counter, fps = 0, 0
		start_time = time.time()

		# Start capturing video input from the camera
		self.cap = cv2.VideoCapture(0)
		self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 576)
		self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 576)
		# self.cap = cv2.VideoCapture(camera_id)
		# self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
		# self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

		# Visualization parameters
		row_size = 20  # pixels
		left_margin = 24  # pixels
		text_color = (0, 255, 0)  # red
		font_size = 2
		font_thickness = 2
		fps_avg_frame_count = 10

		# Initialize the object detection model
		base_options = core.BaseOptions(
			file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
		detection_options = processor.DetectionOptions(
			max_results=3, score_threshold=0.3)
		options = vision.ObjectDetectorOptions(
			base_options=base_options, detection_options=detection_options)
		detector = vision.ObjectDetector.create_from_options(options)

	def on_exit(self):
		print ("leaving object recognition")
		self.cap.release()
		cv2.destroyAllWindows()

	def run(self):
		"""! Continuously run inference on images acquired from the camera.
		@param model Name of the TFLite object detection model.
		@param camera_id The camera id to be passed to OpenCV.
		@param width The width of the frame captured from the camera.
		@param height The height of the frame captured from the camera.
		@param num_threads The number of CPU threads to run the model.
		@param enable_edgetpu True/False whether the model is a EdgeTPU model.
		"""

	def next_frame(self,screen,curr_events,**kwargs):
		self.next_screen_name=self.name
		self.kwarg_handler(kwargs)
		self.blit_all_buttons(screen)
		pressed_button=self.handle_events(screen,curr_events)

		FONT_FEDERATION.render_to(screen, (150, 67), 'Machine Vision', ORANGE,style=0,size=40)
		FONT_FEDERATION.render_to(screen, (150, 117), 'Object Detection', DARK_YELLOW,style=0,size=34)

		# self.run()

		while self.cap.isOpened():
			success, image = self.cap.read()
			if not success:
				sys.exit(
					'ERROR: Unable to read from webcam. Please verify your webcam settings.'
				)

			counter += 1
			image = cv2.flip(image, 1)

			# Convert the image from BGR to RGB as required by the TFLite model.
			rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			# Create a TensorImage object from the RGB image.
			input_tensor = vision.TensorImage.create_from_array(rgb_image)

			# Run object detection estimation using the model.
			detection_result = detector.detect(input_tensor)

			# Draw keypoints and edges on input image
			image = utils.visualize(image, detection_result)



			# Calculate the FPS
			if counter % fps_avg_frame_count == 0:
				end_time = time.time()
				fps = fps_avg_frame_count / (end_time - start_time)
				start_time = time.time()

			# Show the FPS
			fps_text = 'FPS = {:.1f}'.format(fps)
			text_location = (left_margin, row_size)
			cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
					  font_size, text_color, font_thickness)

			# # Stop the program if the ESC key is pressed.
			# k=cv2.waitKey(1)
			# if ((k == 27)):
			#   break

			# cv2.imshow('object_detector', image)

			# print (cvimage_to_pygame(image))
			screen.blit (cvimage_to_pygame(image),(0,0))
			pygame.display.update()


		return self.next_screen_name,self.kwargs
