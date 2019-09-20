# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
from serialization.database_serializer import DatabaseSerializer



class DatabaseSerializerTests(unittest.TestCase):
    def test_highway_merging(self):
        # last params must be only passed for testing purposes not for release!
        dbs = DatabaseSerializer(test_scenarios=1, test_world_steps=10, serialize_scenarios=1)
        dbs.process("database")


if __name__ == '__main__':
    unittest.main()
