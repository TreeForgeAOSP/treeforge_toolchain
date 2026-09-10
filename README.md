# TreeForge Toolchain

Source, build recipes, patches, provenance, compliance metadata, and
provider publication definitions for Android-derived TreeForge tools.

## Principles

- Every AOSP-derived tool is tied to an exact upstream Android release
  and exact source revisions.
- Pristine AOSP builds remain immutable reference baselines.
- TreeForge-modified tools preserve their exact source delta.
- TreeForge-original source is stored directly in this repository.
- A developer must be able to reconstruct the complete build workspace
  and rebuild every published TreeForge tool.
- Runtime use of published providers must not require an AOSP checkout.
- Compiled release binaries are published as release assets rather than
  treated as the authoritative source.

## Android 15 baseline

Canonical upstream baseline:

    android-15.0.0_r36

Pristine reference providers:

    aosp-adb
    aosp-fastboot
    aosp-adbd
    aosp-adbd-recovery
    aosp-fastbootd

TreeForge variants:

    treeforge-adb
    treeforge-fastboot
    treeforge-adbd
    treeforge-fastbootd

Additional TreeForge runtime:

    treeforge-vabc-coordinator
