# Copyright (c) 2019 fortiss GmbH
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import argparse
from serialization.database_serializer import DatabaseSerializer

DATABASE_ROOT = "database"

def main(version, github_token, delete):
    dbs = DatabaseSerializer(test_scenarios=1, test_world_steps=10)
    dbs.process(DATABASE_ROOT)
    dbs.release(version=version,github_token=github_token, delete=delete)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = 'Database serialization')
    parser.add_argument('tag', type=str, help='specifies tag used for release', )
    parser.add_argument('--token', type=str, required=False, default=None,
                         help='if you want to do a github release, specify a github token')
    parser.add_argument('--delete', required=False, default=False, action='store_true',
                         help='true if you want to delete a previous release with the same tag')
    args = parser.parse_args()
    main(args.tag, args.token, args.delete)