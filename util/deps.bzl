load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def benchmark_database_dependencies():
    _maybe(
    native.new_local_repository,
    name = "python_linux",
    path = "./util/venv/",
    build_file_content = """
cc_library(
    name = "python-lib",
    srcs = glob(["lib/libpython3.*", "libs/python3.lib", "libs/python36.lib"]),
    hdrs = glob(["include/**/*.h", "include/*.h"]),
    includes = ["include/python3.6m", "include", "include/python3.7m", "include/python3.5m"],
    visibility = ["//visibility:public"],
)
        """
    )


    _maybe(
    http_archive,
    name = "ghr",
    urls = [" https://github.com/tcnksm/ghr/releases/download/v0.13.0/ghr_v0.13.0_linux_386.tar.gz"],
    strip_prefix="ghr_v0.13.0_linux_386",
    build_file_content = """
filegroup(
    name = "ghr_binary",
    srcs = glob(["**/**"]),
    visibility = ["//visibility:public"],
)
    """
    )


def _maybe(repo_rule, name, **kwargs):
    if name not in native.existing_rules():
        repo_rule(name = name, **kwargs)