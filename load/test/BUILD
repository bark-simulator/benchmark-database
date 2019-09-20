
py_test(
  name = "database_load_test",
  srcs = ["database_load_test.py"],
  data = ['@bark_project//python:bark.so',
          '//database:database'],
  imports = ['../python/'],
  deps = ["//load:benchmark_database",
          "//serialization:database_serializer"],
)

