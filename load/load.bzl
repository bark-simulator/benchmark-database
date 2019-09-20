load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def benchmark_database_release():
    _maybe(
    http_archive,
    name = "benchmark_database_release",
    urls = ["https://github.com/bark-simulator/benchmark-database/releases/download/v1.0.0/benchmark_database_v1.0.0.zip"],
#    strip_prefix="ghr_v0.13.0_linux_386",
    build_file_content = """
filegroup(
    name = "v1.0.0",
    srcs = glob(["**/**"]),
    visibility = ["//visibility:public"],
)
    """
    )


def _maybe(repo_rule, name, **kwargs):
    if name not in native.existing_rules():
        repo_rule(name = name, **kwargs)