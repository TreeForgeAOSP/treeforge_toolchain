# Payload not stored in Git

This provider's compiled payload is intentionally not tracked in the
`treeforge_toolchain` Git repository.

The canonical `snapuserd_ramdisk` payload is built from the pinned Android
source revision and published as a provider-specific GitHub Release asset.

Git retains only the metadata, provenance, legal material, source identity,
and rebuild evidence required to reproduce and verify the release.

Generated binaries belong under `out/` and generated release packages under
`dist/`; both are excluded from Git.
