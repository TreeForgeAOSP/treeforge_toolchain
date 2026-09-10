# Reproducibility

Every TreeForge-modified Android tool must publish enough information to
reconstruct its source and build environment.

Required records:

1. Android platform release/tag.
2. Exact upstream repository revisions.
3. Upstream source paths.
4. Exact TreeForge source patches.
5. TreeForge-original source files.
6. Soong module identities.
7. Build product and build variant.
8. Build commands.
9. Toolchain/compiler identity.
10. Compliance and NOTICE records.
11. Source-sharing records.
12. Output SHA-256 identities.

AOSP source itself is retrieved from Google's public Android repositories
and is not vendored wholesale into this repository.
