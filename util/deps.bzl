load("@bazel_tools//tools/build_defs/repo:git.bzl", "git_repository")

def benchmark_database_dependencies():
    # local repository added like this
    _maybe(
    native.local_repository,
    name = "bark_project",
    path="/home/bernhard/development/bark",
    )

def _maybe(repo_rule, name, **kwargs):
    if name not in native.existing_rules():
        repo_rule(name = name, **kwargs)