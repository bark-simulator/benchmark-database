# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
from serialization.scenario_set_serializer import ScenarioSetSerializer
from modules.runtime.commons.parameters import ParameterServer

class ImporterTests(unittest.TestCase):
    def test_highway_merging(self):
        scenario_param_file =os.path.join("database","scenario_sets", "highway_merging", "ego_alone_on_right.json")
        param_server = ParameterServer(filename = scenario_param_file)
        scenario_set_serializer = ScenarioSetSerializer(params=param_server)

        scenario_set_serializer.dump(os.path.join("database", "scenario_sets", "highway_merging"))
        scenario_set_serializer.load()
        scenario_set_serializer.test()
if __name__ == '__main__':
    unittest.main()
