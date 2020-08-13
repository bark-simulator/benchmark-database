
py_test(
  name = "database_load_local_test",
  srcs = ["database_load_local_test.py"],
  data = ['@bark_project//bark:generate_core',
          '//data/database1:database1'],
  imports = [],
  deps = ["//load:benchmark_database",
          "//serialization:database_serializer"],
)

py_test(
  name = "database_load_github_test",
  srcs = ["database_load_github_test.py"],
  data = ['@bark_project//bark:generate_core',
          "@benchmark_database_release//:v2.0"],
  imports = [],
  deps = ["//load:benchmark_database",
          "//serialization:database_serializer"],
)

