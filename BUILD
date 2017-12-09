load("@io_bazel_rules_docker//python:image.bzl", "py_image")
load("@io_bazel_rules_docker//container:container.bzl", "container_image")

# Script that fails to run
py_image(
    name = "hello_py",
    srcs = ["hello.py"],
    main = "hello.py",
)

container_image(
    name="distroless_with_ldconfig",
    debs=["@libc_bin//file"],
    base="@py_image_base//image",
)

# Also fails
py_image(
    name = "hello_py_with_ldconfig",
    srcs = ["hello.py"], 
    main = "hello.py",
    base = ":distroless_with_ldconfig",
)

container_image(
    name="distroless_with_ldconfig_and_cache",
    debs=["@libc_bin//file"],
    files=[":ld.so.cache"],
    directory="/etc",
    mode="0644",
    base=":distroless_with_ldconfig",
)

# Works!!!
py_image(
    name = "hello_py_with_ldconfig_and_cache",
    srcs = ["hello.py"], 
    main = "hello.py",
    base = ":distroless_with_ldconfig_and_cache",
)

container_image(
    name="distroless_with_dash",
    debs=["@dash//file"],
    base="@py_image_base//image",
)

# Miraculously also works!!!
py_image(
    name = "hello_py_with_dash",
    srcs = ["hello.py"], 
    main = "hello.py",
    base = ":distroless_with_dash",
)
