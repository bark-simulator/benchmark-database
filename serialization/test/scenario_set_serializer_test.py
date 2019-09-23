# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
from serialization.scenario_set_serializer import ScenarioSetSerializer
from modules.runtime.commons.parameters import ParameterServer

class ScenarioSetSerializerTests(unittest.TestCase):
    def test_highway_merging(self):
        scenario_param_file =os.path.join("database","scenario_sets", "highway_merging", "velocity_2_8.json")
        param_server = ParameterServer(filename = scenario_param_file)
        param_server["Scenario"]["Generation"]["NumScenarios"] = 1 # set this down to reduce test runtime
        scenario_set_serializer = ScenarioSetSerializer(params=param_server)

        scenario_set_serializer.dump(os.path.join("database", "scenario_sets", "highway_merging"))
        scenario_set_serializer.load()
        scenario_set_serializer.test(num_scenarios=1, num_steps=5)
if __name__ == '__main__':
    unittest.main()
