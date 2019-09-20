py_library(
  name = "benchmark_database",
  srcs = ["benchmark_database.py"],
  data = ['@bark_project//python:bark.so'],
  imports = ['../python/'],
  deps = [
      "@bark_project//modules/runtime/scenario/scenario_generation:scenario_generation"
    ],
  visibility = ["//visibility:public"],
)