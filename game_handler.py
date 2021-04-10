from settings import cfg

import time, io, re
from os import listdir

import numpy as np
import pytesseract, cv2
from mss import mss
from PIL import Image, ImageChops
import pyautogui




"""
Game interface
Maybe make interface for sct, idk

"""
class game_handler:

	def __init__(self):

		self.img_g_count = 0
		self.img_s_count = 0


	"""
		Make image handler maybe i dont fucking know
	"""
	def create_test_text_data(self):

		data_dir_in = "./tesseract_custom_model/doodle_digits/"
		data_dir_out = "./tesseract_custom_model/doodle_digits_text/"

		cnt = 0

		for i in listdir(data_dir_in):

			cnt += 1

			name = i[:-4]

			file_name = name + ".gt.txt"
			text = ""

			pos_d = name.find('_d')

			if pos_d != -1:
				name = name[:pos_d]
				text = ''.join(re.findall('[0-9]+', name))
			else:
				text = ''.join(re.findall('[0-9]+', name))

			# print(str(cnt) + ". " + file_name + ": " + text)

			outF = open(data_dir_out + file_name, "w")
			outF.write(text)
			outF.close()



	"""
		Make image handler maybe i dont fucking know
	"""
	def create_test_data(self):

		data_dir_in = "./tesseract_custom_model/doodle_digits_backup/"
		data_dir_out = "./tesseract_custom_model/doodle_digits/"

		for i in listdir(data_dir_in):

			if i == ".DS_Store":
				continue

			img = Image.open(data_dir_in + i)

			img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
			cv2.imwrite(data_dir_out + i[:-4] + "_d1.png", img)

			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			cv2.imwrite(data_dir_out + i[:-4] + "_d2.png", img) 

			img = cv2.medianBlur(img, 5)
			cv2.imwrite(data_dir_out + i[:-4] + "_d3.png", img) 

			kernel = np.ones((5,5),np.uint8)
			img = cv2.dilate(img, kernel, iterations = 1)
			cv2.imwrite(data_dir_out + i[:-4] + "_d4.png", img) 

			kernel = np.ones((5,5),np.uint8)
			img = cv2.erode(img, kernel, iterations = 1)
			cv2.imwrite(data_dir_out + i[:-4] + "_d5.png", img) 

			kernel	= np.ones((5,5),np.uint8)
			img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
			cv2.imwrite(data_dir_out + i[:-4] + "_d6.png", img) 

			img = cv2.Canny(img, 100, 200)
			cv2.imwrite(data_dir_out + i[:-4] + "_d7.png", img)

			# img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			# cv2.imwrite(data_dir_out + i[:-4] + "_d8.png", img) 

	"""
		2 Presses to focues on window
	"""
	def start_game(self):

		self._left_click(cfg["game"]["start"])
		self._left_click(cfg["game"]["start"])
		time.sleep(3)
		self._left_click(cfg["game"]["play"])
		time.sleep(1)

	"""
		Actually just clicking is more performent. IDK think about it 
	"""
	def on_death_play_again(self):

		# if self.is_dead():
		self._left_click(cfg["game"]["play_again"])

	"""
		Optimize the unnecessary safe away
	"""
	def is_dead(self):
		
		with mss() as sct:

			sct_img = sct.grab(cfg["game"]["over"])

			img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')

			# img.save("images/img_d.jpg")
			img_dead = Image.open('./images/img_dead.jpg')

			img.save("images/img_d.jpg")
			img = Image.open('./images/img_d.jpg')

			diff = ImageChops.difference(img, img_dead)
			if diff.getbbox():
				print('alive')
				return False
			else:
				print('ded')
				return True

	"""
		Takes one state. You should call it 4 times at once.
		ToDo: 
			- PUT with mss() as sct: before function call
			- Turn into numpy array
	"""
	def get_screen_img(self, count):

		images = []

		with mss() as sct:

			for i in range(count):

				# sct.compression_level = 2
				sct_img = sct.grab(cfg["game"]["screen"])	# returns Screenshot

				img = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')#.convert('LA')
				# img.save("images/img_g_{}.png".format(self.img_g_count))

				self.img_g_count += 1
				images.append(img)

		return images

	"""
		Get Score
		ToDo:
			- get good ocr
			- Turn score into int
	"""
	def get_score(self):
		
		with mss() as sct:

			# sct.compression_level = 1

			# get image and make cv2
			sct_img = sct.grab(cfg["game"]["score"])
			img = cv2.cvtColor(np.array(sct_img), cv2.COLOR_RGB2BGR)
			# cv2.imwrite("images/img_s_{}.jpg".format(self.img_g_count), img) 
			cv2.imwrite("images/img_LOOK_AT_ME.jpg", img)
			# self.img_g_count += 1
			# print("1 Score: " + pytesseract.image_to_string(img, 
			# 	lang="doodle-model", config='tessedit_char_whitelist=0123456789'))



			img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			# cv2.imwrite("images/img_s_{}.jpg".format(self.img_g_count), img) 
			# self.img_g_count += 1
			# print("2 Score: " + pytesseract.image_to_string(img, 
			# 	lang="doodle-model", config='tessedit_char_whitelist=0123456789'))


			img = cv2.medianBlur(img, 5)
			# cv2.imwrite("images/img_s_{}.jpg".format(self.img_g_count), img) 
			# self.img_g_count += 1
			print("3 Score: " + pytesseract.image_to_string(img, 
				lang="doodle-model", config='tessedit_char_whitelist=0123456789'))


			# kernel = np.ones((5,5),np.uint8)
			# img = cv2.dilate(img, kernel, iterations = 1)
			# cv2.imwrite("images/img_s_{}.jpg".format(self.img_g_count), img) 
			# self.img_g_count += 1
			# print("4 Score: " + pytesseract.image_to_string(img, 
				# lang="doodle-model", config='tessedit_char_whitelist=0123456789'))
 

			# kernel = np.ones((5,5),np.uint8)
			# img = cv2.erode(img, kernel, iterations = 1)
			# cv2.imwrite("images/img_s_{}.jpg".format(self.img_g_count), img) 
			# self.img_g_count += 1
			# print("5 Score: " + pytesseract.image_to_string(img, 
			# 	lang="doodle-model", config='tessedit_char_whitelist=0123456789'))


			# kernel	= np.ones((5,5),np.uint8)
			# img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
			# cv2.imwrite("images/img_s_{}.jpg".format(self.img_g_count), img) 
			# self.img_g_count += 1
			# print("6 Score: " + pytesseract.image_to_string(img, 
			# 	lang="doodle-model", config='tessedit_char_whitelist=0123456789'))



			# img = cv2.Canny(img, 100, 200)
			# cv2.imwrite("images/img_s_{}.jpg".format(self.img_g_count), img) 
			# self.img_g_count += 1
			# print("7 Score: " + pytesseract.image_to_string(img, 
			# 	lang="doodle-model", config='tessedit_char_whitelist=0123456789'))


			return img

	def handle_action(self, action):

		print(action)

		if action == 0:
			return
		elif action == 1:
			pyautogui.keyDown('left')
			time.sleep(0.05)
			pyautogui.keyUp('left')
		elif action == 2:
			pyautogui.keyDown('right')
			time.sleep(0.05)
			pyautogui.keyUp('right')
		elif action == 3:
			pyautogui.mouseDown()
			time.sleep(0.01)
			pyautogui.mouseUp()
		
	def _left_click(self, coord):
		x, y = coord
		pyautogui.mouseDown(x, y)
		time.sleep(cfg["click"]["wait_between_press"])
		pyautogui.mouseUp()
		time.sleep(cfg["click"]["wait_between_press"])
 