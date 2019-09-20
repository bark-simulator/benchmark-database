# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging

from modules.runtime.scenario.scenario_generation.scenario_generation import ScenarioGeneration
from modules.runtime.scenario.scenario_generation.uniform_vehicle_distribution import UniformVehicleDistribution
from modules.runtime.scenario.scenario_generation.deterministic import DeterministicScenarioGeneration
from modules.runtime.commons.parameters import ParameterServer
import modules.runtime.scenario.scenario_generation 

FILE_EXTENSION_SCENARIO_SET = "bark_scenarios"

# The ScenarioSetSerializer dumps, loads and tests all scenarios sets specified in one param file


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
        return "{}_{}_{}.{}".format(set_name, num_scenarios, seed, FILE_EXTENSION_SCENARIO_SET)

    def dump(self, dir):
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

    def load(self, filename=None):
        if not filename and self._last_serialized_filename:
            filename = self._last_serialized_filename
        self._scenario_generator = ScenarioGeneration()
        self._scenario_generator.load_scenario_list(filename=filename)

    def test(self):
        if not self._scenario_generator:
            logging.error("No scenario generator initialized for testing")
            return

        logging.info("Testing {} with seed {} from generator {}".format(
            self._set_name, self._generator_seed, self._scenario_generator_name
        ))
        for _ in range(0, self._num_scenarios): # run all scenarios
            scenario, idx = self._scenario_generator.get_next_scenario()
            world_state = scenario.get_world_state()
            logging.info("Running scenario {} of {} in set {}".format(idx,
                                                                 self._scenario_generator.num_scenarios,
                                                                 self._set_name))
            for _ in range(0, 100): # run a few steps for each scenario
                world_state.step(self._simulation_step_time)


