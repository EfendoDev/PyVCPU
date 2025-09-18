import wowtell1025 as cpu

# Sample config, dont be scared to modify

rom_file=open(input("ROM => ")+".rom")

rom=[]
for line in rom_file:
	read_line=line.strip()
	if r"\n" in read_line:
		rom.append(read_line.replace(r"\n","\n"))
	elif r"\r" in read_line:
		rom.append(read_line.replace(r"\r","\r"))
	else:
		rom.append(read_line)
	
cpu.run(rom, cpu.firmware)
