# Binary payload policy

Provider: `aosp-adbd`
Release: `android-15.0.0_r36-arm64`

Canonical payload:

    rootfs/system/apex/com.android.adbd.capex

Accepted SHA-256:

    77999007b945dcf69d87f2f23c56276d7f3e7dbc9f5b0d5bc940c72daa3302f4

The compiled payload is intentionally not copied into the ordinary
source/publication tree.

Published payloads will be generated from the pinned source and build
recipe and distributed as immutable GitHub Release assets.

TreeForge will download the exact provider release, verify its archive
identity, verify all internal payload identities, and cache it for use.
