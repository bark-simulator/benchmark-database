# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging
import subprocess
logging.getLogger().setLevel(logging.INFO)
import argparse
import zipfile
import shutil

from modules.runtime.commons.parameters import ParameterServer
from serialization.scenario_set_serializer import ScenarioSetSerializer
FILE_EXTENSION_SCENARIO_SET = "bark_scenarios"

# The DatabaseSerializer recursively serializes all scenario param files sets
# within a folder and releases the whole database as zip file to github


class DatabaseSerializer:
    def __init__(self, test_scenarios, test_world_steps, num_serialize_scenarios=None, visualize_tests=False, viewer=None):
        self._test_scenarios = test_scenarios
        self._test_world_steps = test_world_steps
        self._visualize_tests = visualize_tests
        self._database_dir = None
        self._viewer = viewer

        # provides a way to reduce the generated scenarios for each param file for unittesting
        self._num_serialize_scenarios = num_serialize_scenarios 

    def _process_folder(self, dir):
        process_result = True
        for root, dirs, files in os.walk(dir):
            for name in files:
                if name.endswith(".json"):
                    process_result = process_result and \
                           self._process_json_paramfile(os.path.join(root, name))
            for dir in dirs:
                process_result = process_result and self._process_folder(dir)
        return process_result

    def _process_json_paramfile(self, param_filename):
        param_server = ParameterServer(filename = param_filename)
        if self._num_serialize_scenarios:
            # set this down to reduce test runtime !Only for Unittesting!
            param_server["Scenario"]["Generation"]["NumScenarios"] = self._num_serialize_scenarios 

        scenario_set_serializer = ScenarioSetSerializer(params=param_server)
        scenario_set_serializer.dump(os.path.dirname(param_filename))
        scenario_set_serializer.load()
        return scenario_set_serializer.test(num_scenarios=self._test_scenarios,
                                     num_steps=self._test_world_steps,
                                     visualize_test=self._visualize_tests,
                                     viewer=self._viewer)
    
    def process(self, database_dir):
        self._database_dir = database_dir
        return self._process_folder(database_dir)

    @staticmethod
    def _release_file_name(version):
        return "benchmark_database_{}".format(version)

    @staticmethod
    def _pack(database_dir, packed_file_name):
        logging.info('The following list of files will be released:')
        zipf = zipfile.ZipFile(packed_file_name, 'w', zipfile.ZIP_DEFLATED)
        tmp_dir = "/tmp/database/"  
        if os.path.exists(tmp_dir):
            shutil.rmtree(tmp_dir)
        shutil.copytree(database_dir, tmp_dir) # copy to resolve symlinks
        for root, dirs, files in os.walk(tmp_dir):
            for file in files:
                if file.endswith(".zip"):
                    continue # do not include our own created zip file
                zip_root = root.replace("/tmp/","")
                logging.info(os.path.join(zip_root, file))
                zipf.write(os.path.join(zip_root, file))
        logging.info("Packed release file {}".format(os.path.abspath(packed_file_name)))

    @staticmethod
    def _github_release(database_file, version, github_token, delete):
        if delete:
            delete_cmd = "-delete"
        else:
            delete_cmd = ""
        print(os.getcwd())
        ghr_command = os.path.abspath("external/ghr")
        full_file_path = os.path.abspath(database_file)
        os.chdir(ghr_command)
        ghr_full_command = "./ghr -t {} -u bark-simulator -r benchmark-database {} {} {}".format(
           github_token, delete_cmd, version, full_file_path)
        out = subprocess.call(ghr_full_command, shell=True)
        logging.info("Release output {}".format(out))

    def release(self, version, github_token=None, delete=False):
        if self._num_serialize_scenarios:
            logging.warning("Do not set down the number of serialized scenarios in a release \
                    -> set serialized_scenarios=None")

        if not self._database_dir:
            logging.error("No database dir given, call process first.")

        packed_file_name = os.path.join(self._database_dir,"{}.{}".format(
            DatabaseSerializer._release_file_name(version), "zip"))
        DatabaseSerializer._pack(self._database_dir, packed_file_name)

        if github_token:
            DatabaseSerializer._github_release(packed_file_name, version, github_token, delete)
        else:
            logging.info("Assuming local release as you did not provide a github token.")

        return packed_file_name

