#!/usr/bin/env python3
from __future__ import annotations

from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path
import json
import shutil


EXPECTED_BUSYBOX_SHA256 = (
    "531d479411a97d90186a08ad2f873e3f"
    "3c48a4b569f100dccfecead5d56e49ac"
)


def digest(path: Path) -> str:
    return sha256(
        path.read_bytes()
    ).hexdigest()


def main() -> int:
    parser = ArgumentParser()

    parser.add_argument(
        "--rootfs",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--busybox",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--applets",
        required=True,
        type=Path,
    )

    parser.add_argument(
        "--manifest",
        required=True,
        type=Path,
    )

    args = parser.parse_args()

    rootfs = args.rootfs.resolve()
    busybox = args.busybox.resolve()
    applets_file = args.applets.resolve()
    manifest_path = args.manifest.resolve()

    if not busybox.is_file():
        raise RuntimeError(
            f"BusyBox missing: {busybox}"
        )

    actual = digest(
        busybox
    )

    if actual != EXPECTED_BUSYBOX_SHA256:
        raise RuntimeError(
            "BusyBox identity drift: "
            f"{actual}"
        )

    applets = tuple(
        line.strip()
        for line
        in applets_file.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    )

    if not applets:
        raise RuntimeError(
            "BusyBox applet contract is empty"
        )

    system_bin = (
        rootfs
        / "system"
        / "bin"
    )

    system_bin.mkdir(
        parents=True,
        exist_ok=True,
    )

    target = (
        system_bin
        / "busybox"
    )

    shutil.copy2(
        busybox,
        target,
    )

    target.chmod(
        0o755
    )

    records = []

    for applet in applets:
        if (
            not applet
            or "/"
            in applet
        ):
            raise RuntimeError(
                f"invalid applet name: {applet!r}"
            )

        link = (
            system_bin
            / applet
        )

        if (
            link.exists()
            or link.is_symlink()
        ):
            link.unlink()

        link.symlink_to(
            "busybox"
        )

        if not link.is_symlink():
            raise RuntimeError(
                f"symlink creation failed: {link}"
            )

        if link.readlink() != Path(
            "busybox"
        ):
            raise RuntimeError(
                f"wrong symlink target: {link}"
            )

        records.append(
            {
                "applet": applet,
                "path": (
                    "rootfs/system/bin/"
                    + applet
                ),
                "target": "busybox",
            }
        )

    manifest = {
        "schema_version": 1,
        "busybox": {
            "path":
                "rootfs/system/bin/busybox",
            "sha256": actual,
        },
        "applet_count":
            len(records),
        "applets":
            records,
    }

    manifest_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    manifest_path.write_text(
        json.dumps(
            manifest,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"busybox_sha256={actual}"
    )
    print(
        f"applet_count={len(records)}"
    )
    print(
        f"manifest={manifest_path}"
    )
    print(
        "BUSYBOX_APPLET_SYMLINKS=PASS"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
