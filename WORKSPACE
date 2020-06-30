workspace(name = "benchmark_database")


load("//util:deps.bzl", "benchmark_database_dependencies")
benchmark_database_dependencies()

load("//load:load.bzl", "benchmark_database_release")
benchmark_database_release()

load("@bark_project//tools:deps.bzl", "bark_dependencies")
bark_dependencies()

load("@com_github_nelhage_rules_boost//:boost/boost.bzl", "boost_deps")
boost_deps()




