
py_test(
  name = "serialization_test",
  srcs = ["serialization_test.py"],
  data = ['@bark_project//python:bark.so',
          '//maps:xodr_data',
          '//scenario_sets:scenario_sets'],
  imports = ['../python/'],
  deps = ["//serialization:serializer"],
)