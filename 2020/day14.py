import re
import os
from collections import defaultdict


regex = re.compile(r"([a-z\[\]0-9]+) = ([X0-9]+)$")
regex2 = re.compile(r"(\d+)")


def binary(int_):
    return str(bin(int(int_))[2:]).zfill(36)


def integer(bin_):
    return int("0b" + bin_, 2)


def part1(lines):
    mem = defaultdict(lambda: "0" * 36)
    for line in lines:
        group1, group2 = regex.match(line).groups()
        if group1 == "mask":
            bitmask = group2
        else:
            addr = int(regex2.search(group1).group(1))
            value = int(group2)
            bin_ = binary(value)
            new_value = ""
            for bit, mask in zip(list(bin_), list(bitmask)):
                if mask == "X":
                    new_value += bit
                else:
                    new_value += mask
            mem[addr] = new_value
    total = 0
    for value in mem.values():
        total += integer(value)
    return total


def part2(lines):
    mem = defaultdict(lambda: "0" * 36)
    for line in lines:
        group1, group2 = regex.match(line).groups()
        if group1 == "mask":
            bitmask = group2
        else:
            addr = int(regex2.search(group1).group(1))
            value = int(group2)
            bin_addr = binary(addr)
            masked_address = ""
            for addr_bit, mask_bit in zip(list(bin_addr), list(bitmask)):
                if mask_bit == "X":
                    masked_address += "X"
                elif mask_bit == "1":
                    masked_address += "1"
                else:
                    masked_address += addr_bit
            addresses = [""]
            for addr_bit in masked_address:
                if addr_bit in ["0", "1"]:
                    addresses = [addr + addr_bit for addr in addresses]
                else:
                    new_addresses = [addr + "0" for addr in addresses]
                    old_addresses = [addr + "1" for addr in addresses]
                    addresses = new_addresses + old_addresses
            for addr in addresses:
                mem[integer(addr)] = value
    total = 0
    for value in mem.values():
        total += value
    return total


def main():
    with open(os.path.join("data", "day14.txt")) as f:
        lines = [line.strip() for line in f]

    print(part1(lines))
    print(part2(lines))


if __name__ == "__main__":
    main()
