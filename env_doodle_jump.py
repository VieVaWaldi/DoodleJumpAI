from game_handler import game_handler
import enum


class actions(enum.Enum):
    skip = 0
    left = 1
    right = 2
    shoot = 3


class env_doodle_jump:

	def __init__(self):
		
		self.game_handler = game_handler()

	def reset(self):
		pass

	def step(self, action):

		# do action
		self.game_handler.handle_action(action)

		# get reward
		self.game_handler.get_score()

		# get state
		for i in range(4):
			self.game_handler.get_screen_img()

	def get_observation_space(self):
		pass

	def get_actions(self):
		return actions