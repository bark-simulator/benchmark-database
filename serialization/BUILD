py_library(
  name = "scenario_set_serializer",
  srcs = ["scenario_set_serializer.py"],
  imports = [],
  deps = ["@bark_project//bark/runtime/commons:parameters",
          "@bark_project//bark/runtime/commons:xodr_parser",
          "@bark_project//bark/runtime/viewer:matplotlib_viewer",
          "@bark_project//bark/runtime/scenario/scenario_generation:scenario_generation"],
  visibility = ["//visibility:public"],
)


py_library(
  name = "database_serializer",
  srcs = ["database_serializer.py"],
  data = ["@ghr//:ghr_binary"],
  imports = [],
  deps = ["@bark_project//bark/runtime/commons:parameters",
          ":scenario_set_serializer"],
  visibility = ["//visibility:public"],
)


py_binary(
  name = "release",
  srcs = ["release.py"],
  data = ['@bark_project//bark:generate_core',
          '//data/data2/database2:database2'],
  imports = [],
  deps = [":database_serializer"],
  visibility = ["//visibility:public"],
)


