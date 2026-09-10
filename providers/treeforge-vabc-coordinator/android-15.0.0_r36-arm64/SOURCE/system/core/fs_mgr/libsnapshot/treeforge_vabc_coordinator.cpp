/*
 * TreeForge Virtual A/B Recovery Coordinator
 *
 * Android baseline:
 *   android-15.0.0_r36
 *
 * This initial provider milestone is intentionally NON-DESTRUCTIVE.
 * It proves the statically-linked full-COW libsnapshot closure and
 * TreeForge's Recovery-specific IDeviceInfo boundary.
 *
 * Snapshot creation, COW mapping, writes, FinishedSnapshotWrites(),
 * and slot activation are not reachable from this probe version.
 */

#include <cstdio>
#include <memory>
#include <string>

#include <libdm/dm.h>
#include <liblp/partition_opener.h>
#include <libsnapshot/snapshot.h>

namespace {

using android::snapshot::ISnapshotManager;
using android::snapshot::SnapshotManager;


class TreeForgeRecoveryDeviceInfo final
    : public SnapshotManager::IDeviceInfo {
  public:
    using MergeStatus =
        SnapshotManager::IDeviceInfo::MergeStatus;

    TreeForgeRecoveryDeviceInfo(
        std::string slot_suffix,
        std::string super_device,
        std::string metadata_dir
    )
        : slot_suffix_(std::move(slot_suffix)),
          super_device_(std::move(super_device)),
          metadata_dir_(std::move(metadata_dir)) {}

    std::string GetMetadataDir() const override {
        return metadata_dir_;
    }

    std::string GetSlotSuffix() const override {
        return slot_suffix_;
    }

    std::string GetOtherSlotSuffix() const override {
        return (
            slot_suffix_ == "_a"
            ? "_b"
            : "_a"
        );
    }

    std::string GetSuperDevice(
        [[maybe_unused]] uint32_t slot
    ) const override {
        return super_device_;
    }

    const android::fs_mgr::IPartitionOpener&
    GetPartitionOpener() const override {
        return opener_;
    }

    bool IsOverlayfsSetup() const override {
        return false;
    }

    bool SetBootControlMergeStatus(
        [[maybe_unused]] MergeStatus status
    ) override {
        /*
         * Fail closed. The preparation coordinator does not own
         * boot-control state.
         */
        return false;
    }

    bool SetActiveBootSlot(
        [[maybe_unused]] unsigned int slot
    ) override {
        /*
         * Hard safety boundary: TreeForge Recovery performs slot
         * activation separately and explicitly.
         */
        return false;
    }

    bool SetSlotAsUnbootable(
        [[maybe_unused]] unsigned int slot
    ) override {
        return false;
    }

    bool IsRecovery() const override {
        return true;
    }

    bool AllowVirtualAbInRecovery() const override {
        return true;
    }

    bool IsFirstStageInit() const override {
        return false;
    }

    std::unique_ptr<IImageManager>
    OpenImageManager() const override {
        return (
            ISnapshotManager::IDeviceInfo
                ::OpenImageManager("ota")
        );
    }

    android::dm::IDeviceMapper&
    GetDeviceMapper() override {
        return android::dm::DeviceMapper::Instance();
    }

    bool IsTempMetadata() const override {
        return false;
    }

  private:
    std::string slot_suffix_;
    std::string super_device_;
    std::string metadata_dir_;

    android::fs_mgr::PartitionOpener opener_;
};


bool ParseArgument(
    const char* argument,
    const char* prefix,
    std::string* output
) {
    std::string value(argument);

    std::string expected(prefix);

    if (value.rfind(expected, 0) != 0) {
        return false;
    }

    *output = value.substr(expected.size());

    return true;
}

}  // namespace


int main(int argc, char** argv) {
    std::string slot_suffix;
    std::string super_device =
        "/dev/block/by-name/super";
    std::string metadata_dir =
        "/metadata/ota";

    bool probe = false;

    for (int index = 1; index < argc; ++index) {
        std::string argument(argv[index]);

        if (argument == "--probe") {
            probe = true;
            continue;
        }

        if (
            ParseArgument(
                argv[index],
                "--slot=",
                &slot_suffix
            )
        ) {
            continue;
        }

        if (
            ParseArgument(
                argv[index],
                "--super=",
                &super_device
            )
        ) {
            continue;
        }

        if (
            ParseArgument(
                argv[index],
                "--metadata=",
                &metadata_dir
            )
        ) {
            continue;
        }

        std::fprintf(
            stderr,
            "unknown argument: %s\\n",
            argv[index]
        );

        return 2;
    }

    if (!probe) {
        std::fprintf(
            stderr,
            "treeforge-vabc-coordinator: "
            "only --probe is enabled in this milestone\\n"
        );

        return 2;
    }

    if (
        slot_suffix != "_a"
        && slot_suffix != "_b"
    ) {
        std::fprintf(
            stderr,
            "--slot must be _a or _b\\n"
        );

        return 2;
    }

    auto* device =
        new TreeForgeRecoveryDeviceInfo(
            slot_suffix,
            super_device,
            metadata_dir
        );

    /*
     * SnapshotManager takes ownership of IDeviceInfo.
     *
     * Construction itself is non-destructive: no BeginUpdate(),
     * CreateUpdateSnapshots(), mapping, COW write, finalization,
     * or boot-control operation is called here.
     */
    auto manager =
        SnapshotManager::New(device);

    if (!manager) {
        std::fprintf(
            stderr,
            "unable to construct SnapshotManager\\n"
        );

        return 3;
    }

    std::printf(
        "treeforge-vabc-coordinator-v1\\n"
    );

    std::printf(
        "mode=probe\\n"
    );

    std::printf(
        "slot=%s\\n",
        slot_suffix.c_str()
    );

    std::printf(
        "other_slot=%s\\n",
        device->GetOtherSlotSuffix().c_str()
    );

    std::printf(
        "super=%s\\n",
        super_device.c_str()
    );

    std::printf(
        "metadata=%s\\n",
        metadata_dir.c_str()
    );

    std::printf(
        "is_recovery=1\\n"
    );

    std::printf(
        "allow_virtual_ab_in_recovery=1\\n"
    );

    std::printf(
        "full_cow_build=1\\n"
    );

    std::printf(
        "snapshot_creation=disabled\\n"
    );

    std::printf(
        "cow_write=disabled\\n"
    );

    std::printf(
        "slot_activation=disabled\\n"
    );

    return 0;
}
