py_library(
  name = "scenario_set_serializer",
  srcs = ["scenario_set_serializer.py"],
  data = ['@bark_project//python:bark.so'],
  imports = ['../python/'],
  deps = ["@bark_project//modules/runtime/commons:parameters",
          "@bark_project//modules/runtime/commons:xodr_parser",
          "@bark_project//modules/runtime/scenario/scenario_generation:scenario_generation"],
  visibility = ["//visibility:public"],
)


py_library(
  name = "database_serializer",
  srcs = ["database_serializer.py"],
  data = ['@bark_project//python:bark.so'],
  imports = ['../python/'],
  deps = ["@bark_project//modules/runtime/commons:parameters",
          ":scenario_set_serializer"],
  visibility = ["//visibility:public"],
)


