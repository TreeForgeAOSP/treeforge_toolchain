# kexec-tools

TreeForge provider for the upstream kexec-tools 2.0.32 userspace loader.

The provider payload is a fully static Linux ARM64 `kexec` executable
intended for TreeForge early-userspace consumers such as Bootstrap.

Build with:

    ./scripts/build-kexec-tools

Package only this provider with:

    TREEFORGE_PACKAGE_PROVIDER=kexec-tools ./scripts/package
