#!/bin/sh

mkdir -p unpacked
cd unpacked
cpio -idv < ../../challenge/initramfs.cpio

# Create /root/flag.txt
mkdir root && cd root && echo 'hxp{DUMMY}' > flag.txt
