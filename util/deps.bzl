load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")
load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

def benchmark_database_dependencies():
    # local repository added like this
    _maybe(
    native.local_repository,
    name = "bark_project",
    path="/home/bernhard/development/bark",)

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