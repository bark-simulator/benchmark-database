# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from serialization.scenario_set_serializer import ScenarioSetSerializer
from bark.runtime.commons.parameters import ParameterServer
from bark.runtime.scenario.scenario_generation.scenario_generation import ScenarioGeneration
from bark.runtime.scenario import SetMapfileDirectory
import uuid
import zipfile
import pickle
import os
import pandas as pd
import logging
import shutil
logging.getLogger().setLevel(logging.INFO)

# The DatabaseSerializer recursively serializes all scenario param files sets
# within a folder and releases the whole database as zip file to github


class BenchmarkDatabase:
    def __init__(self, database_root=None, dataframe=None):
        if database_root and not isinstance(dataframe, pd.DataFrame):
            self._init_from_database_root(database_root)
        elif isinstance(dataframe, pd.DataFrame) and database_root:
            self._init_from_dataframe(dataframe, database_root)
        else:
            raise ValueError("Invalid argument combination \
                        for initialization of database")

    def _init_from_database_root(self, database_root):
        self.database_root = database_root
        if not os.path.exists(database_root):
            logging.error("Given database root does not exist")
            return
        if database_root.endswith("zip"):
            #tmp_dir_path = "../tmp/bark_extracted_databases/" # # /tmp not available on cluster
            tmp_dir_path = "/tmp/bark_extracted_databases/"
            tmp_dir_name = tmp_dir_path + "{}".format(uuid.uuid4())
            logging.info(
                "extracting zipped-database {} to temporary directory {}".format(database_root, tmp_dir_name))
            os.makedirs(tmp_dir_name)
            with zipfile.ZipFile(database_root, 'r') as zip_obj:
                zip_obj.extractall(tmp_dir_name)
            self.database_root = tmp_dir_name

        # parse recursively all info dictionaries in database into pandas table
        self.dataframe = pd.DataFrame()
        for root, dirs, files in os.walk(self.database_root):
            for file in files:
                if ScenarioSetSerializer.scenario_set_info_fileprefix() in file:
                    logging.info("Found info dict {}".format(file))
                    with open(os.path.join(root, file), "rb") as f:
                        info_dict = pickle.load(f)
                    self.dataframe = self.dataframe.append(
                        info_dict, ignore_index=True)
        logging.info("The following scenario sets are available")
        logging.info("\n"+self.dataframe.to_string())

    def _init_from_dataframe(self, dataframe, database_root):
        self.database_root = database_root
        self.dataframe = dataframe

    def get_num_scenario_sets(self):
        return len(self.dataframe.index)

    def get_scenario_generator(self, scenario_set_id):
        serialized_file_name = self.dataframe.iloc[scenario_set_id]["Serialized"]
        if os.path.exists(serialized_file_name):
            serialized_file_path = serialized_file_name
        else:
            serialized_file_path = os.path.join(
                self.database_root, serialized_file_name)
        cwd = None
        if os.path.exists(self.database_root):
            # move into database root that map files can be found
            cwd = os.getcwd()
            os.chdir(self.database_root)
        param_file_name = self.dataframe.iloc[scenario_set_id]["Params"]
        if not param_file_name:
            logging.warning("No param file found for scenario set {}. Using defaults...".format(
                self.dataframe.iloc[scenario_set_id]["SetName"]))
            params = ParameterServer()
        else:
            params = ParameterServer(filename=param_file_name)

        scenario_generation = ScenarioGeneration(params=params)
        scenario_generation.load_scenario_list(filename=serialized_file_name)
        SetMapfileDirectory(self.database_root)
        if cwd:
            os.chdir(cwd)
        scenario_set_name = self.dataframe.iloc[scenario_set_id]["SetName"]
        scenario_set_parameters = self.dataframe.iloc[scenario_set_id]["SetParameters"]
        return scenario_generation, scenario_set_name, scenario_set_parameters

    def __iter__(self):
        self.current_iter_idx = 0
        # An iterator interface to loop over all contained scenario sets
        return self

    def __next__(self):
        if self.current_iter_idx < self.get_num_scenario_sets():
            scenario_generator = self.get_scenario_generator(
                self.current_iter_idx)
            self.current_iter_idx += 1
            return scenario_generator
        else:
            raise StopIteration

    def apply_filter(self, pattern, **kwargs):
        dataframe = self.dataframe[self.dataframe['SetName'].str.contains(
            pat=pattern, **kwargs)]
        return BenchmarkDatabase(database_root=self.database_root,
                                 dataframe=dataframe)
