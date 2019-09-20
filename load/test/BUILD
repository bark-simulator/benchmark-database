
py_test(
  name = "database_load_test",
  srcs = ["database_load_test.py"],
  data = ['@bark_project//python:bark.so',
          '//database:database',
          "@benchmark_database_release//:v1.0.0"],
  imports = ['../python/'],
  deps = ["//load:benchmark_database",
          "//serialization:database_serializer"],
)

