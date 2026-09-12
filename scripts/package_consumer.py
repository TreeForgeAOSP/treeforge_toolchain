#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shutil
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
ASSETS = DIST / "assets"
PROVIDERS = ROOT / "providers"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for chunk in iter(
            lambda: handle.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def safe_extract(
    archive: Path,
    destination: Path,
) -> None:
    with tarfile.open(
        archive,
        "r:xz",
    ) as handle:
        for member in handle.getmembers():
            member_path = Path(member.name)

            if (
                member_path.is_absolute()
                or ".." in member_path.parts
            ):
                raise RuntimeError(
                    f"unsafe archive path: {member.name}"
                )

            if (
                member.issym()
                or member.islnk()
            ):
                raise RuntimeError(
                    f"archive links are not permitted: "
                    f"{member.name}"
                )

        handle.extractall(
            destination,
            filter="data",
        )


def normalized_manifest(
    provider: str,
    release: str,
) -> Path | None:
    candidate = (
        PROVIDERS
        / provider
        / release
        / "manifest.json"
    )

    if not candidate.is_file():
        return None

    try:
        data = json.loads(
            candidate.read_text()
        )
    except Exception:
        return None

    if (
        data.get("schema") != 2
        or data.get("name") != provider
        or data.get("release") != release
    ):
        return None

    return candidate


def write_internal_sha256(
    root: Path,
) -> None:
    ledger = root / "SHA256SUMS"

    records: list[str] = []

    for path in sorted(
        p
        for p in root.rglob("*")
        if p.is_file()
        and p != ledger
    ):
        relative = path.relative_to(root)

        records.append(
            f"{sha256_file(path)}  "
            f"{relative.as_posix()}"
        )

    ledger.write_text(
        "\n".join(records)
        + "\n"
    )


def write_deterministic_archive(
    source_root: Path,
    archive: Path,
    epoch: int,
) -> None:
    temporary = (
        archive.parent
        / f".{archive.name}.tmp"
    )

    temporary.unlink(
        missing_ok=True
    )

    with tarfile.open(
        temporary,
        "w:xz",
        format=tarfile.PAX_FORMAT,
    ) as handle:
        paths = [
            source_root,
            *sorted(
                source_root.rglob("*"),
                key=lambda path: (
                    path.relative_to(
                        source_root
                    ).as_posix()
                ),
            ),
        ]

        for path in paths:
            if path == source_root:
                archive_name = source_root.name
            else:
                archive_name = (
                    source_root.name
                    + "/"
                    + path.relative_to(
                        source_root
                    ).as_posix()
                )

            info = handle.gettarinfo(
                str(path),
                arcname=archive_name,
            )

            info.uid = 0
            info.gid = 0
            info.uname = ""
            info.gname = ""
            info.mtime = epoch

            if path.is_file():
                with path.open("rb") as stream:
                    handle.addfile(
                        info,
                        stream,
                    )
            else:
                handle.addfile(info)

    os.replace(
        temporary,
        archive,
    )


def finalize_consumer_manifests() -> None:
    index_path = DIST / "index.json"

    if not index_path.is_file():
        raise RuntimeError(
            f"dist index unavailable: {index_path}"
        )

    index = json.loads(
        index_path.read_text()
    )

    providers = index.get(
        "providers"
    )

    if not isinstance(
        providers,
        list,
    ):
        raise RuntimeError(
            "dist index providers must be a list"
        )

    epoch = int(
        index["source_date_epoch"]
    )

    finalized = 0

    for entry in providers:
        provider = entry["provider"]

        platform = entry["platform"]

        release = (
            index["android_release"]
            + "-"
            + platform
        )

        manifest = normalized_manifest(
            provider,
            release,
        )

        archive = (
            ASSETS
            / entry["archive"]
        )

        if manifest is None:
            entry[
                "consumer_manifest"
            ] = False
            continue

        with tempfile.TemporaryDirectory(
            prefix="treeforge-package-consumer-"
        ) as raw:
            temporary_root = Path(raw)

            safe_extract(
                archive,
                temporary_root,
            )

            package_root = (
                temporary_root
                / f"{provider}-{release}"
            )

            if not package_root.is_dir():
                raise RuntimeError(
                    "release package root is unavailable: "
                    f"{package_root}"
                )

            consumer_root = (
                package_root
                / "consumer"
            )

            consumer_root.mkdir(
                parents=True,
                exist_ok=True,
            )

            shutil.copy2(
                manifest,
                consumer_root
                / "manifest.json",
            )

            write_internal_sha256(
                package_root
            )

            write_deterministic_archive(
                package_root,
                archive,
                epoch,
            )

        digest = sha256_file(
            archive
        )

        entry["archive_sha256"] = digest
        entry["archive_bytes"] = (
            archive.stat().st_size
        )
        entry["consumer_manifest"] = True

        sidecar = (
            archive.with_name(
                archive.name
                + ".sha256"
            )
        )

        sidecar.write_text(
            f"{digest}  {archive.name}\n"
        )

        finalized += 1

    index["provider_count"] = len(
        providers
    )

    index_path.write_text(
        json.dumps(
            index,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    )

    combined = []

    for entry in sorted(
        providers,
        key=lambda item: item["archive"],
    ):
        combined.append(
            f"{entry['archive_sha256']}  "
            f"{entry['archive']}"
        )

    (
        DIST
        / "SHA256SUMS"
    ).write_text(
        "\n".join(combined)
        + "\n"
    )

    print(
        "consumer_manifests_finalized="
        f"{finalized}"
    )


if __name__ == "__main__":
    finalize_consumer_manifests()
