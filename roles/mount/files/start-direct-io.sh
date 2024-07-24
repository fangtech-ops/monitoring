#!/bin/bash

set -euo pipefail

error() {
    (>&2 echo "$@")
    exit 1
}

if [[ -z "$1" ]]; then
    error "Must supply mountpoint"
fi

MNTPT=$1

DEVICE=$(df | grep -w $MNTPT | awk '{print $1}') || true
if [[ -z "$DEVICE" ]]; then
    error "$MNTPT not found"
elif [[ "$DEVICE" != *"loop"* ]]; then
    error "Device $DEVICE is not a loop device for $MNTPT"
else
    echo "Turning on direct i/o for $DEVICE"
    losetup --direct-io=on $DEVICE
fi

