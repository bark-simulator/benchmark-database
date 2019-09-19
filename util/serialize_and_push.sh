#bazel run //serialization/test:serialization_test
GITHUB_TOKEN=
PROJECT_USERNAME=bark-simulator
PROJECT_REPONAME=benchmark-database
ARTIFACT_PATH=./bazel-out/k8-fastbuild/bin/serialization/test/serialization_test.runfiles/benchmark_database/scenario_sets/serialized/highway_merging

ghr -t ${GITHUB_TOKEN} -u ${PROJECT_USERNAME} -r ${PROJECT_REPONAME} -delete v0.01 ${ARTIFACT_PATH}
