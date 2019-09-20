# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
from load.benchmark_database import BenchmarkDatabase
from serialization.database_serializer import DatabaseSerializer



class DatabaseSerializerTests(unittest.TestCase):
    def test_get_highway_merging_generator(self):
        # release the database
        dbs = DatabaseSerializer(test_scenarios=1, test_world_steps=10, num_serialize_scenarios=1)
        dbs.process("database")
        local_release_filename = dbs.release(version="0.0.1")

    
        # then reload to test correct parsing
        db = BenchmarkDatabase(local_release_filename)
        scenario_generation = db.get_scenario_generator(scenario_set_id=0)

if __name__ == '__main__':
    unittest.main()
