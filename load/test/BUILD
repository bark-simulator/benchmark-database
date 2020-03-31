
py_test(
  name = "database_load_local_test",
  srcs = ["database_load_local_test.py"],
  data = ['@bark_project//python:bark.so',
          '//data/database1:database1'],
  imports = ['../python/'],
  deps = ["//load:benchmark_database",
          "//serialization:database_serializer"],
)

py_test(
  name = "database_load_github_test",
  srcs = ["database_load_github_test.py"],
  data = ['@bark_project//python:bark.so',
          "@benchmark_database_release//:v2.0"],
  imports = ['../python/'],
  deps = ["//load:benchmark_database",
          "//serialization:database_serializer"],
)

