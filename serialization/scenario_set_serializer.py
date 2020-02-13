# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging
import random
import pickle


from modules.runtime.scenario.scenario_generation.scenario_generation import ScenarioGeneration
from modules.runtime.scenario.scenario_generation.uniform_vehicle_distribution import UniformVehicleDistribution
from modules.runtime.scenario.scenario_generation.deterministic import DeterministicScenarioGeneration
from modules.runtime.commons.parameters import ParameterServer
import modules.runtime.scenario.scenario_generation 

FILE_EXTENSION_SCENARIO_SET = "bark_scenarios"

# The ScenarioSetSerializer dumps, loads and
# tests all scenarios sets specified in one param file


class ScenarioSetSerializer:
  def __init__(self, params):
    self._params = params
    self._scenario_generator_name = self._params["Scenario"]["Generation"]["GeneratorName"]
    self._generator_seed =  self._params["Scenario"]["Generation"]["GeneratorSeed"]
    self._num_sets =  self._params["Scenario"]["Generation"]["GeneratorName"]
    self._num_scenarios =  self._params["Scenario"]["Generation"]["NumScenarios"]
    self._set_name =   self._params["Scenario"]["Generation"]["SetName"]
    self._simulation_step_time = self._params["simulation"]["step_time"]
    self._scenario_generator = None
    self._last_serialized_filename = None
  
  @staticmethod
  def scenario_file_name(set_name, num_scenarios, seed):
    return "{}_scenarios{}_seed{}.{}".format(set_name, num_scenarios, seed, FILE_EXTENSION_SCENARIO_SET)

  @staticmethod
  def scenario_set_info_filename(set_name):
    return "set_info_{}".format(set_name)

  @staticmethod
  def scenario_set_info_fileprefix():
    return "set_info"

  def dump(self, dir):
    self._dump(dir, self._scenario_generator_name, self._num_scenarios, self._generator_seed)

  def _dump(self, dir, generator, num_scenarios, seed, **kwargs):
    self._scenario_generator = eval("{}( \
            num_scenarios={}, random_seed={}, params=self._params)".format(self._scenario_generator_name,
                                                                self._num_scenarios,
                                                                self._generator_seed))
    filename = os.path.join(dir, ScenarioSetSerializer.scenario_file_name(
      self._set_name, self._num_scenarios, self._generator_seed
    ))
    if not os.path.exists(os.path.dirname(filename)):
      os.makedirs(os.path.dirname(filename))
    self._scenario_generator.dump_scenario_list(filename)
    self._last_serialized_filename = filename

    info_dict = {"GeneratorName": generator, "SetName": self._set_name, "NumScenarios": num_scenarios,
                  "Seed": seed, "Serialized": filename, "Params": self._params.param_filename,
                  **kwargs}

    info_filename = os.path.join(dir, ScenarioSetSerializer.scenario_set_info_filename(self._set_name))
    with open(info_filename, "wb") as f:
      pickle.dump(info_dict , f)

  def load(self, filename=None):
    if not filename and self._last_serialized_filename:
        filename = self._last_serialized_filename
    self._scenario_generator = ScenarioGeneration()
    self._scenario_generator.load_scenario_list(filename=filename)

  def test(self, num_scenarios, num_steps):
    if not self._scenario_generator:
      logging.error("No scenario generator initialized for testing")
      return

    logging.info("Testing {} with seed {} from generator {}".format(
      self._set_name, self._generator_seed, self._scenario_generator_name
    ))

    for _ in range(0, num_scenarios): # run all scenarios
      scenario_idx = random.randint(0, self._num_scenarios-1)
      scenario = self._scenario_generator.GetScenario(scenario_idx)
      world_state = scenario.get_world_state()
      logging.info("Running scenario {} of {} in set {}".format(scenario_idx,
        self._scenario_generator.num_scenarios,
        self._set_name))
      for _ in range(0, num_steps): # run a few steps for each scenario
        world_state.Step(self._simulation_step_time)


