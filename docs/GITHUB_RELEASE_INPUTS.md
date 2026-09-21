# GitHub Release Inputs

TreeForge compiled provider payloads are distributed as GitHub Release assets and are not tracked as source files in Git.

The repository retains the inputs required to reconstruct releases:

- exact Android source revisions
- Android 15 r36 build matrix
- TreeForge patches
- provider metadata
- legal and provenance metadata
- deterministic lifecycle scripts
- source inventory

Generated out, work, and dist directories remain outside Git.

## Lifecycle

1. Run scripts/build.
2. Run scripts/package.
3. Run scripts/verify.
4. Refresh source and provider inventories.
5. Commit all source-side release definitions.
6. Run scripts/package from that exact committed HEAD.
7. Run scripts/verify.
8. Package again and prove identical archive hashes.
9. Push that exact commit.
10. Run scripts/release with the publish option.

scripts/release is read-only unless publication is explicitly requested.

Publication requires:

- complete verification
- clean toolchain worktree
- dist generated from the current HEAD
- origin branch matching that same HEAD
- no existing provider release tags

Existing releases are never overwritten.

Each provider uses an exact provider-specific tag:

<provider>/android-15.0.0_r36-1

Floating latest releases are not part of the contract.

Release manifest.json and normalized consumer/manifest.json are separate contracts.

The final TreeForge consumer lock is generated only after the final toolchain commit has been packaged reproducibly, because each release records its exact toolchain source commit.

## Source repository versus release repository

The canonical source and public release repository is:

TreeForgeAOSP/treeforge_toolchain

The private backup mirror is:

TreeForgeDEV/treeforge_toolchain

TreeForgeAOSP is the authoritative source repository and the home for
published provider release assets. TreeForgeDEV is maintained only as a
private backup mirror and is not a separate source authority.

Release publication may still use `--repository OWNER/REPO` or
`TREEFORGE_RELEASE_REPOSITORY` when an explicit destination override is
required.

SOURCE-REBUILD.json is generated from the exact source commit at package time
and is mandatory release metadata. It is verified independently rather than
having its commit-dependent SHA-256 embedded in the static consumer manifest.
