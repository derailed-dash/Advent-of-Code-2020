a_num = 102
bin_str = bin(a_num)
print(f"Bin representation {bin_str} = {a_num}")

doubled_num = a_num << 1
print(f"Bit shifted left: {bin(doubled_num)} = {doubled_num}")

halved_num = doubled_num >> 1
print(f"Bit shifted right: {bin(halved_num)} = {halved_num}")

halved_num = halved_num >> 1
print(f"Bit shifted right: {bin(halved_num)} = {halved_num}")

halved_num = halved_num >> 1
print(f"Bit shifted right: {bin(halved_num)} = {halved_num}")

# use bit shift to set arbitrary bit position
posn = 8
val = 1 << posn
print(f"1 << {posn} = {bin(val)} = {val}")

subnet_mask = 192
addr = 223
apply_mask = subnet_mask & addr
print(f"Mask\t: {bin(subnet_mask)} = {subnet_mask}")
print(f"Addr\t: {bin(addr)} = {addr}")
print(f"Res\t: {bin(apply_mask)} = {apply_mask}")

for i, subnet_ in enumerate(zip(subnet_mask, addr)):