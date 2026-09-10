# Binary payload policy

Provider: `aosp-adb`
Release: `android-15.0.0_r36-linux-x86_64`

Canonical payload:

    bin/adb

Accepted SHA-256:

    1cf16f6b87dc63e95a83b3b6dce6711fc778b1c04565beb58e182fc21a6910f3

The compiled payload is intentionally not copied into the ordinary
source/publication tree.

Published payloads will be generated from the pinned source and build
recipe and distributed as immutable GitHub Release assets.

TreeForge will download the exact provider release, verify its archive
identity, verify all internal payload identities, and cache it for use.
