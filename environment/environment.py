# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np

class Environment(object):
  # cached action size
  action_size = -1

  LOG_DIR = None

  @staticmethod
  def get_log_dir():
    if Environment.LOG_DIR is None:
      timestamp = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
      Environment.LOG_DIR = './logs/' + timestamp
    return Environment.LOG_DIR

  @staticmethod
  def set_log_dir(dir):
    Environment.LOG_DIR = dir

  @staticmethod
  def create_environment(env_type, env_name, thread_index=0):
    if env_type == 'maze':
      from . import maze_environment
      return maze_environment.MazeEnvironment()
    elif env_type == 'lab':
      from . import lab_environment
      return lab_environment.LabEnvironment(env_name)
    elif env_type == 'indoor':
      from . import indoor_environment
      return indoor_environment.IndoorEnvironment(env_name, thread_index)
    else:
      from . import gym_environment
      return gym_environment.GymEnvironment(env_name)
  
  @staticmethod
  def get_action_size(env_type, env_name):
    if Environment.action_size >= 0:
      return Environment.action_size

    if env_type == 'maze':
      from . import maze_environment
      Environment.action_size = \
        maze_environment.MazeEnvironment.get_action_size()
    elif env_type == "lab":
      from . import lab_environment
      Environment.action_size = \
        lab_environment.LabEnvironment.get_action_size(env_name)
    elif env_type == "indoor":
      from . import indoor_environment
      Environment.action_size = \
        indoor_environment.IndoorEnvironment.get_action_size(env_name)
    else:
      from . import gym_environment
      Environment.action_size = \
        gym_environment.GymEnvironment.get_action_size(env_name)
    return Environment.action_size

  def __init__(self):
    pass

  def process(self, action):
    pass

  def reset(self):
    pass

  def stop(self):
    pass  

  def _subsample(self, a, average_width):
    s = a.shape
    sh = s[0]//average_width, average_width, s[1]//average_width, average_width
    return a.reshape(sh).mean(-1).mean(1)  

  def _calc_pixel_change(self, state, last_state):
    d = np.absolute(state[2:-2,2:-2,:] - last_state[2:-2,2:-2,:])
    # (80,80,3)
    m = np.mean(d, 2)
    c = self._subsample(m, 4)
    return c
