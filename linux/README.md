Tool to facilitate interaction between the Linux kernel and QEMU

Usage: linux-qemu [-cdgh]

Options:
    -c     run qemu in current console
    -g     have qemu start up a gdb server
    -d     start gdb and connect to QEMU server
    -h     show help and exit

Environment Variables:
    LINUX: Path to Linux source tree
    INITRAMFS: A cpio'd initramfs for the kernel to boot into
