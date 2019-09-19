# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
from serialization.serializer import Serializer
from modules.runtime.commons.parameters import ParameterServer

class ImporterTests(unittest.TestCase):
    def test_highway_merging(self):
        scenario_param_file =os.path.join("scenario_sets", "highway_merging", "ego_alone_on_right.json")
        param_server = ParameterServer(filename = scenario_param_file)
        serializer = Serializer(params=param_server)

        serializer.dump(os.path.join("scenario_sets","serialized","highway_merging"))
        serializer.load()
        serializer.test()
if __name__ == '__main__':
    unittest.main()
