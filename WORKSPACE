git_repository(
    name = "io_bazel_rules_docker",
    remote = "https://github.com/bazelbuild/rules_docker.git",
    commit = "f133b0cfcc29f08e1819490428f66a2e956f4d35",
)

load(
    "@io_bazel_rules_docker//python:image.bzl",
    _py_image_repos = "repositories",
)

_py_image_repos()


# Specific Debian packages we want to add
http_file(
  name="libc_bin",
  url="http://http.us.debian.org/debian/pool/main/g/glibc/libc-bin_2.24-11+deb9u1_amd64.deb",
  sha256="1908a1b6092a0681e914bc02d5b52bceebb48d8e40203f97ae8cedf80694fd6f",
)

http_file(
  name="dash",
  url="http://http.us.debian.org/debian/pool/main/d/dash/dash_0.5.8-2.4_amd64.deb",
  sha256="5084b7e30fde9c51c4312f4da45d4fdfb861ab91c1d514a164dcb8afd8612f65",
)
