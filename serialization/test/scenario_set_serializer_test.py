# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
import matplotlib
from serialization.scenario_set_serializer import ScenarioSetSerializer
from bark.runtime.commons.parameters import ParameterServer

class ScenarioSetSerializerTests(unittest.TestCase):
    def test_highway_merging(self):
        current_working_dir = os.getcwd()
        database_root = os.path.join("data","database1")
        os.chdir(database_root)
        scenario_param_file =os.path.join("scenario_sets", "highway_merging", "20per_variation.json")
        param_server = ParameterServer(filename = scenario_param_file)
        param_server["Scenario"]["Generation"]["NumScenarios"] = 1 # set this down to reduce test runtime
        scenario_set_serializer = ScenarioSetSerializer(params=param_server)

        scenario_set_serializer.dump(os.path.join("data","database1","scenario_sets", "highway_merging"))
        scenario_set_serializer.load()
        test_result = scenario_set_serializer.test(num_scenarios=1, num_steps=5, visualize_test=False)
        self.assertTrue(test_result)
        test_result = scenario_set_serializer.test(num_scenarios=1, num_steps=5, visualize_test=True)
        self.assertTrue(test_result)
        os.chdir(current_working_dir)
if __name__ == '__main__':
    unittest.main()
