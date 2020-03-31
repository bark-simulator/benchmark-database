# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
from serialization.database_serializer import DatabaseSerializer



class DatabaseSerializerTests(unittest.TestCase):
    def test_database1(self):
        # last params must be only passed for testing purposes not for release!
        dbs = DatabaseSerializer(test_scenarios=1, test_world_steps=10, num_serialize_scenarios=1)
        test_result = dbs.process("data/database1")
        self.assertTrue(test_result)
        dbs.release(version="0.0.1")

    def test_database2(self):
        # last params must be only passed for testing purposes not for release!
        dbs = DatabaseSerializer(test_scenarios=1, test_world_steps=10, num_serialize_scenarios=1)
        test_result = dbs.process("data/data2/database2")
        self.assertTrue(test_result)
        dbs.release(version="0.0.1")


if __name__ == '__main__':
    unittest.main()
