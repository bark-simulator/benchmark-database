# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging
import random
import pickle
import time


from modules.runtime.scenario.scenario_generation.scenario_generation import ScenarioGeneration
from modules.runtime.scenario.scenario_generation.uniform_vehicle_distribution import UniformVehicleDistribution
from modules.runtime.scenario.scenario_generation.deterministic import DeterministicScenarioGeneration
from modules.runtime.scenario.scenario_generation.configurable_scenario_generation import ConfigurableScenarioGeneration
from modules.runtime.commons.parameters import ParameterServer
from modules.runtime.viewer.matplotlib_viewer import MPViewer


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
                num_scenarios={}, params=self._params, random_seed={})".format(self._scenario_generator_name,
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
                     "Seed": seed, "Serialized": filename, "Params": self._params.param_filename, **kwargs}

        info_filename = os.path.join(dir, ScenarioSetSerializer.scenario_set_info_filename(self._set_name))
        with open(info_filename, "wb") as f:
            pickle.dump(info_dict , f)

    def load(self, filename=None):
        if not filename and self._last_serialized_filename:
            filename = self._last_serialized_filename
        self._scenario_generator = ScenarioGeneration()
        self._scenario_generator.load_scenario_list(filename=filename)

    def test(self, num_scenarios, num_steps, visualize_test, viewer=None):
        if not self._scenario_generator:
            logging.error("No scenario generator initialized for testing")
            return

        logging.info("Testing {} with seed {} from generator {}".format(
            self._set_name, self._generator_seed, self._scenario_generator_name
        ))

        results = []
        for _ in range(0, num_scenarios ): # run all scenarios
            scenario_idx = random.randint(0, self._num_scenarios-1)
            result = self._test_scenario(scenario_idx, num_steps, visualize_test, viewer)
            results.append(result)

        failed = not all(results)
        failed_scenario_idx = [idx for idx, rst in enumerate(results) if rst == False]
        if failed:
            logging.error("Failed scenario indexes {} during testing of {} with seed {} and generator {}".format(
            failed_scenario_idx, self._set_name, self._generator_seed, self._scenario_generator_name))
            return False
        return True


    def _test_scenario(self, scenario_idx, num_steps, visualize, viewer):
            logging.info("Running scenario {} of {} in set {}".format(scenario_idx,
                                                                self._scenario_generator.num_scenarios,
                                                                self._set_name))
            try:
                scenario = self._scenario_generator.get_scenario(scenario_idx)
            except Exception as e:
                logging.error("Deserialization failed with {}.".format(e))
                return False
            try:
                world_state = scenario.get_world_state()
            except Exception as e:
                logging.error("Get world state failed with {}.".format(e))
                return False

            if visualize:
                if not viewer:
                  viewer = MPViewer(
                  params=ParameterServer(),
                  x_range=[5060, 5160],
                  y_range=[5070,5150],
                  use_world_bounds=True)

            sim_step_time = 0.2
            sim_real_time_factor = 1

            try:
                for _ in range(0, num_steps): # run a few steps for each scenario
                  if visualize:
                        viewer.drawWorld(world_state, scenario._eval_agent_ids)
                        viewer.show(block=False)
                        time.sleep(sim_step_time/sim_real_time_factor)
                  world_state.Step(sim_step_time)
                return True
            except Exception as e:
                logging.error("Simulation failed with {}.".format(e))
                return False


