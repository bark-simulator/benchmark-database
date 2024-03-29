# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import logging
import glob
import uuid
import subprocess
logging.getLogger().setLevel(logging.INFO)
import argparse
import zipfile
import shutil

from bark.runtime.commons.parameters import ParameterServer
from serialization.scenario_set_serializer import ScenarioSetSerializer
FILE_EXTENSION_SCENARIO_SET = "bark_scenarios"

# The DatabaseSerializer recursively serializes all scenario param files sets
# within a folder and releases the whole database as zip file to github


class DatabaseSerializer:
    def __init__(self, test_scenarios, test_world_steps, num_serialize_scenarios=None, test_scenario_idxs=None,
                                                               visualize_tests=False, viewer=None):
        self._test_scenarios = test_scenarios
        self._test_world_steps = test_world_steps
        self._test_scenario_idxs = test_scenario_idxs
        self._visualize_tests = visualize_tests
        self._database_dir = None
        self._viewer = viewer

        # provides a way to reduce the generated scenarios for each param file for unittesting
        self._num_serialize_scenarios = num_serialize_scenarios 

    def _process_folder(self, databasedir, filter_sets=None):
        process_result = 0
        if filter_sets:
            files = glob.glob(os.path.join(databasedir, filter_sets), recursive=True)
        else:
            files = glob.glob(os.path.join(databasedir, "**/*.json"), recursive=True)
        for name in files:
            if name.endswith(".json"):
                if self._process_json_paramfile(name):
                    process_result +=1
        return process_result

    def _clean_old_files(self, databasedir):
        file_types_to_clean = ["**/*.bark_scenarios", "**/set_info_*"]
        for file_type in file_types_to_clean:
            files = glob.glob(os.path.join(databasedir, file_type), recursive=True)
            for file in files:
                os.remove(file)

    def _process_json_paramfile(self, param_filename, json=None):
        if json:
            param_server = ParameterServer(json = json)
        else:
            param_server = ParameterServer(filename = param_filename)
        if self._num_serialize_scenarios:
            # set this down to reduce test runtime !Only for Unittesting!
            param_server["Scenario"]["Generation"]["NumScenarios"] = self._num_serialize_scenarios 
        current_dir = os.getcwd()
        os.chdir(self._database_dir)
        scenario_set_serializer = ScenarioSetSerializer(params=param_server)
        scenario_set_serializer.dump(os.path.relpath(os.path.dirname(param_filename), self._database_dir))
        scenario_set_serializer.load()
        test_result = scenario_set_serializer.test(num_scenarios=self._test_scenarios,
                                     num_steps=self._test_world_steps,
                                     visualize_test=self._visualize_tests,
                                     viewer=self._viewer,
                                     test_scenario_idxs=self._test_scenario_idxs)
        os.chdir(current_dir)
        return test_result
    
    def _process_scenario_list(self, database_dir, scenario_set_dict):
        serialized_sets_dir = os.path.join(database_dir, "scenario_sets")
        if not os.path.exists(serialized_sets_dir):
            os.makedirs(serialized_sets_dir)
        process_result = True
        for scenario_set, json_params in scenario_set_dict.items():
            json_params["Scenario"]["Generation"]["SetName"] = scenario_set
            params = ParameterServer(json=json_params)
            filename = os.path.join(serialized_sets_dir, "{}.json".format(scenario_set))
            print(filename)
            params.save(filename)
            process_result = process_result and \
                    self._process_json_paramfile(filename, json=json_params)
        return process_result

    def _process_scenario_generators(self, database_dir, scenario_generator_list):
        serialized_sets_dir = os.path.join(database_dir, "scenario_sets", "from_scenario_generation")
        if not os.path.exists(serialized_sets_dir):
            os.makedirs(serialized_sets_dir)
        process_result = True
        current_dir = os.getcwd()
        os.chdir(database_dir)
        for idx, scenario_generator in enumerate(scenario_generator_list):
            scenario_set_serializer = ScenarioSetSerializer(scenario_generator=scenario_generator)
            scenario_set_serializer.dump(os.path.relpath(serialized_sets_dir, database_dir))
            scenario_set_serializer.load()
            process_result = process_result and \
                     scenario_set_serializer.test(num_scenarios=self._test_scenarios,
                                     num_steps=self._test_world_steps,
                                     visualize_test=self._visualize_tests,
                                     viewer=self._viewer,
                                     test_scenario_idxs=self._test_scenario_idxs)
        os.chdir(current_dir)
        return process_result

    def process(self, database_dir, scenario_set_dict=None, scenario_generator_list=None, filter_sets=None):
        self._clean_old_files(database_dir)
        if not scenario_set_dict and not scenario_generator_list:
            self._database_dir = database_dir
            succ = self._process_folder(database_dir, filter_sets)
        elif database_dir and scenario_set_dict:
            self._database_dir = database_dir # TODO(@Klemens): use serialized_sets_dir?
            succ = self._process_scenario_list(database_dir, scenario_set_dict)
        elif database_dir and scenario_generator_list:
            self._database_dir = database_dir # TODO(@Klemens): use serialized_sets_dir?
            succ = self._process_scenario_generators(database_dir, scenario_generator_list)
        else:
            raise ValueError("Invalid argument combination.")
        return succ

    @staticmethod
    def _release_file_name(version):
        return "benchmark_database_{}".format(version)

    @staticmethod
    def _pack(database_dir, packed_file_name, tmp_dir=None):
        logging.info('The following list of files will be released:')
        zipf = zipfile.ZipFile(packed_file_name, 'w', zipfile.ZIP_DEFLATED)
        tmp_dir = tmp_dir or "/tmp"
        packing_folder = os.path.join(tmp_dir, "packed_databases/{}".format(uuid.uuid4()))
        shutil.copytree(database_dir, packing_folder) # copy to resolve symlinks
        for subdir, dirs, files in os.walk(packing_folder):
            for file in files:
                filepath = os.path.join(subdir, file)
                if filepath.endswith(".zip"):
                    continue # do not include our own created zip file or BUILD
                zip_root = filepath.replace(packing_folder,"")
                logging.info(os.path.join(zip_root, file))
                zipf.write(os.path.join(subdir, file), zip_root)
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

    def release(self, version, github_token=None, delete=False, tmp_dir = None):
        if self._num_serialize_scenarios:
            logging.warning("Do not set down the number of serialized scenarios in a release \
                    -> set serialized_scenarios=None")

        if not self._database_dir:
            logging.error("No database dir given, call process first.")

        packed_file_name = os.path.join(os.path.dirname(self._database_dir),"{}.{}".format(
            DatabaseSerializer._release_file_name(version), "zip"))
        DatabaseSerializer._pack(self._database_dir, packed_file_name, tmp_dir)

        if github_token:
            DatabaseSerializer._github_release(packed_file_name, version, github_token, delete)
        else:
            logging.info("Assuming local release as you did not provide a github token.")
        self._clean_old_files(self._database_dir)
        return packed_file_name

