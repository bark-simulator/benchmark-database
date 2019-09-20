
py_test(
  name = "scenario_set_serializer_test",
  srcs = ["scenario_set_serializer_test.py"],
  data = ['@bark_project//python:bark.so',
          '//database:database'],
  imports = ['../python/'],
  deps = ["//serialization:scenario_set_serializer"],
)

py_test(
  name = "database_serializer_test",
  srcs = ["database_serializer_test.py"],
  data = ['@bark_project//python:bark.so',
          '//database:database'],
  imports = ['../python/'],
  deps = ["//serialization:database_serializer"],
)