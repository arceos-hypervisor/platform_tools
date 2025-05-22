#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0
# Copyright (c) 2019 Fuzhou Rockchip Electronics Co., Ltd.

import os
import argparse
import subprocess
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--bsp', required=True, help='bsp path, relative to rockchip directory')
    parser.add_argument('--kernel', required=True, help='kernel image path')
    parser.add_argument('--dst', required=True, help='output img path')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))

    print(f"  Script  dir: {script_dir}")
    dst_dir = Path( os.path.realpath(args.dst))

    print(f"  Destination: {dst_dir}")

    dst_dir.mkdir(parents=True, exist_ok=True)

    bsp_dir = os.path.join(script_dir, args.bsp)
    cpu_dir = Path(bsp_dir).parent
    dtb_name = os.path.basename(bsp_dir) + ".dtb"
    dtb_path = os.path.join(bsp_dir, dtb_name)

    print(f"  CPU: {cpu_dir}")
    print(f"  BSP: {bsp_dir}")

    boot_its_tmp = os.path.join( cpu_dir, "boot.its")

    boot_its_file = os.path.join(dst_dir, "boot.its")

    kernel_path = os.path.realpath(args.kernel)

    res_dir = os.path.join(bsp_dir, "resource.img")

    print(f"Using {boot_its_tmp}")
    print(f"Dest {boot_its_file}")

    with open(boot_its_tmp, "r") as f:
        boot_its = f.read()
        boot_its = boot_its.replace("@DTB@", dtb_path)
        boot_its = boot_its.replace("@KERNEL@", kernel_path)
        boot_its = boot_its.replace("@RESOURCE@", res_dir)

        with open(boot_its_file, "w") as f:
            f.write(boot_its)

    mkimage = "mkimage"
    mkimage_arg = "-E -p 0x800"
    cmd = f"{mkimage} {mkimage_arg} -f {boot_its_file} {os.path.join(dst_dir, 'boot.img')}"
    print(f"  Command: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

if __name__ == "__main__":
    main()