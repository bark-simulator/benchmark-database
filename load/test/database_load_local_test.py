# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import unittest
import os
import sys
from load.benchmark_database import BenchmarkDatabase
from serialization.database_serializer import DatabaseSerializer



class DatabaseSerializerTests(unittest.TestCase):
    def test_database_from_local_release(self):
        # release the database
        dbs = DatabaseSerializer(test_scenarios=1, test_world_steps=10, num_serialize_scenarios=1)
        dbs.process("data/database1")
        local_release_filename = dbs.release(version="0.0.1")

    
        # then reload to test correct parsing
        db = BenchmarkDatabase(database_root=local_release_filename)
        scenario_generation, _, set_parameters = db.get_scenario_generator(scenario_set_id=1)
        self.assertEqual(db.get_num_scenario_sets(), 2)
        self.assertEqual(set_parameters["Test1"], 200)
        self.assertEqual(set_parameters["Test2"], 0.5)

        db_filtered = db.apply_filter("40")
        self.assertEqual(db_filtered.get_num_scenario_sets(), 1)

        for scenario_generation, _, params in db:
            print(scenario_generation)


if __name__ == '__main__':
    unittest.main()
