import os

vs = {
				"ABI_LIBC_VERSION":    "glibc_2.19",
				"ABI_VERSION":         "gcc",
				"BAZEL_COMPILER":      "gcc",
				"BAZEL_HOST_SYSTEM":   "i686-unknown-linux-gnu",
				"BAZEL_TARGET_CPU":    "k8",
				"BAZEL_TARGET_LIBC":   "glibc_2.19",
				"BAZEL_TARGET_SYSTEM": "x86_64-unknown-linux-gnu",
				"CC":                  "gcc",
				"CC_TOOLCHAIN_NAME":   "linux_gnu_x86"
}

for a, b in vs.items():
    print("export " + a +"=" + b)


