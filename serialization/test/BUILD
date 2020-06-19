
py_test(
  name = "scenario_set_serializer_test",
  srcs = ["scenario_set_serializer_test.py"],
  data = ['@bark_project//bark/python_wrapper:core.so',
          '//data/database1:database1'],
  imports = [],
  deps = ["//serialization:scenario_set_serializer"],
)

py_test(
  name = "database_serializer_test",
  srcs = ["database_serializer_test.py"],
  data = ['@bark_project//bark/python_wrapper:core.so',
          '//data/database1:database1',
          '//data/data2/database2:database2'],
  imports = [],
  deps = ["//serialization:database_serializer"],
)