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
    def test_database_from_github_release(self):
        db = BenchmarkDatabase(database_root="external/benchmark_database_release")
        scenario_generation = db.get_scenario_generator(scenario_set_id=0)

if __name__ == '__main__':
    unittest.main()
