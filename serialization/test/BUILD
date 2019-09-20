
py_test(
  name = "serialization_test",
  srcs = ["serialization_test.py"],
  data = ['@bark_project//python:bark.so',
          '//database:database'],
  imports = ['../python/'],
  deps = ["//serialization:scenario_set_serializer"],
)