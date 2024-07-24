# Mount

- Formats the specified `device` as `fstype` (default: *ext4*), then mounts it to `mntpt`.
    - When provided, `mkfs_opts` are passed to Ansible's `filesystem` module.
- If `skip_mounts` is set, then this role does nothing.
