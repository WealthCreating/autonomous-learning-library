import numpy as np

class AccumulatingTraces:
  def __init__(self, env, approximation, decay_rate):
    self.env = env
    self.approximation = approximation
    self.decay_rate = decay_rate
    self.traces = np.zeros(approximation.get_parameters().shape)

  def call(self, *args):
    return self.approximation.call(*args)

  def update(self, *args):
    num_args = len(args) - 1
    error = args[num_args]
    gradient = error * self.approximation.gradient(*(args[0:num_args]))
    return self.update_parameters(gradient)

  def gradient(self, *args):
    return self.approximation.gradient(*args)

  def get_parameters(self):
    return self.approximation.get_parameters()

  def set_parameters(self, parameters):
    self.approximation.set_parameters(parameters)
    return self

  def update_parameters(self, gradient):
    self.traces += gradient
    self.approximation.update_parameters(self.traces)
    self.traces *= 0 if self.env.done else self.decay_rate
    return self
