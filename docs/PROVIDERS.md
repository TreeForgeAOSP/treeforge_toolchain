# Provider Classes

## AOSP_REFERENCE_PROVIDER

Untouched build of an exact AOSP module used as a regression and
reproducibility baseline.

## TREEFORGE_MODIFIED_AOSP_PROVIDER

A provider built from a pinned AOSP baseline plus an explicit TreeForge
source delta.

## TREEFORGE_ORIGINAL_PROVIDER

A provider whose implementation is TreeForge-owned source.

Published binary providers consume the source/build records maintained
by this repository. Source and build recipes remain authoritative.
