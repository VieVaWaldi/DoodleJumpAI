from env_doodle_jump import env_doodle_jump
from game_handler import game_handler

import time, random
from os import listdir

if __name__ == "__main__":

	env = env_doodle_jump()
	game_handler = game_handler()


	# SINGLE FUNCTIONS

	# game_handler.create_test_data()
	# game_handler.create_test_text_data()

	# print("ded") if game_handler.is_dead() else print('alive')

	# while True:
	# 	game_handler.get_score()
	
	# TEST GAME LOOP

	# game_handler.start_game()

	while True:
	
		game_handler.on_death_play_again()

		action = random.randint(0, 4)
		game_handler.handle_action(action)
		game_handler.get_score()



	# TEST GET SCREEN

	# start = time.time()
	# try:
	# 	while True:
	# 		game_handler.get_screen_img(1)
	# except KeyboardInterrupt:
	# 	end = time.time()
	# 	dur = end-start
	# 	img_count = len(listdir("images/"))
	# 	print("Seconds it took: {}".format(dur))
	# 	print("Took {} images for {} images per second".format(img_count, img_count/dur))
