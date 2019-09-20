# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging
import argparse
import zipfile

from modules.runtime.commons.parameters import ParameterServer
from serialization.scenario_set_serializer import ScenarioSetSerializer
FILE_EXTENSION_SCENARIO_SET = "bark_scenarios"

# The DatabaseSerializer recursively serializes all scenario param files sets
# within a folder and releases the whole database as zip file to github


class DatabaseSerializer:
    def __init__(self, test_scenarios, test_world_steps, serialize_scenarios=None):
        self._test_scenarios = test_scenarios
        self._test_world_steps = test_world_steps
        self._database_dir = None

        # provides a way to reduce the generated scenarios for each param file for unittesting
        self._serialize_scenarios = serialize_scenarios 

    def _process_folder(self, dir):
        for root, dirs, files in os.walk(dir):
            for name in files:
                if name.endswith("*.json"):
                    self._process_json_paramfile(name)
            for dir in dirs:
                self._process_folder(dir)

    def _process_json_paramfile(self, param_filename):
        param_server = ParameterServer(filename = param_filename)
        if self._serialized_scenarios:
            # set this down to reduce test runtime !Only for Unittesting!
            param_server["Scenario"]["Generation"]["NumScenarios"] = self._serialize_scenarios 

        scenario_set_serializer = ScenarioSetSerializer(params=param_server)
        scenario_set_serializer.dump(os.path.dirname(param_filename))
        scenario_set_serializer.load()
        scenario_set_serializer.test(num_scenarios=self._test_scenarios,
                                     num_steps=self._test_world_steps)
    
    def process(self, database_dir):
        self._database_dir = database_dir
        self._process_folder(database_dir)

    @staticmethod
    def _release_file_name(version):
        return "benchmark_database_{}".format(version)

    @staticmethod
    def _pack(database_dir, packed_file_name):
        zipf = zipfile.ZipFile(packed_file_name, 'w', zipfile.ZIP_DEFLATED)    
        for root, dirs, files in os.walk(self._database_dir):
            for file in files:
                ziph.write(os.path.join(root, file))

    @staticmethod
    def _release(database_file, version):
        pass

    def release(self, version, github_token=None):
        if self._serialized_scenarios:
            logging.error("Do not set down the number of serialized scenarios in a release \
                    -> set serialized_scenarios=None")
            return

        if not self._database_dir:
            logging.error("No database dir given, call process first.")
        
        # printing the list of all files to be released
        logging.info('The following list of files will be released:')
        # ziph is zipfile handle
        for root, dirs, files in os.walk(self._database_dir):
            for file in files:
                logging.info(file)

        answer = input("Do you want to pack and release these files? [y/Y]")
        if answer.lower() != "y":
            print("Release canceled...")
            return

        packed_file_name = os.path.join(self._database_dir,"{}.{}".format(
            DatabaseSerializer._release_file_name(version, "zip")))
        DatabaseSerializer._pack(self._database_dir, packed_file_name)

        if github_token:
            DatabaseSerializer._release()
        else:
            logging.info("Assuming release test. No actual release takes place.")

        





        
    
  