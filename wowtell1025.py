# This is the first and probably worst CPU for PihOS, but this is the only CPU ill make for now
# Uhhh this is heavily inspired my the late Terry A. Davis (Allah Rahmet Eylesin)
# However unlike him I am bad at programming so im just gonna make this all virtual by just like this making a VCPU
# Also no optimizations for this. Its Currently 23:42 on a school night as im writing this. Im too tired. Fuck you
import os
import random
import time
if os.name == "nt":
	import winsound # SoundAPI just for windows

if os.name =="java":
	print("No, you're not gonna run this.")
	exit

'''
#########################################################################
CPU INFORMATION, I KNOW THIS COULD BE DONE BETTER, BUT I DONT GIVE A FUCK
#########################################################################
'''
brand = "Wowtell"
model = "1025"
ins_set = "SSARIC"
register_count = 6
registers = {
"r1":"00",
"r2":"00",
"r3":"00",
"r4":"00",
"r5":"00",
"r6":"00",
"r7":"00",
"r8":"00"
}
rgstr_max_size = 512
debug = False

'''
#########################################################################
INSTRUCTION SET, VERY BAD, DO NOT TRY TO FIX, YOULL WANT TO DIE, TRUST ME
#########################################################################
'''
instructionset={ # These are 50/50 a todo and 50/50 needed
"01":"print", # implemented
"02":"move", # implemented
"03":"clear", # implemented
"04":"jump", # implemented
"05":"mult", # implemented
"06":"divi", # implemented
"07":"addi", # implemented
"08":"subt", # implemented
"09":"input", # implemented
"0a":"delete", # implemented
"0b":"back", # implemented
"0c":"if", # implemented         # !!! This is for numbers, it will compare R3 and R4
"0d":"random", # implemented
"0e":"add", # implemented
"0f":"modulo", # implemented
"10":"var_if", # implemented      # !!! This is for strings
"11":"index",   # implemented     # !!! This is to get letters/digits from strings/numbers out of a variable and puts it into another
"12":"beep", # implemented        # !!! WINDOWS ONLY
"13":"sleep", # mimimimi          # !!! i went to SLEEP while implementing (Get it hhahahahahahaha im so funny hhahHHAHAHAHAHA)
"14":"index_range", # implemented
"15":"fwrite", # implemented
"16":"fread", # implement
"17":"fcreate", # implemented
"18":"fappend" # implemented
} 

'''
######################
INBUILT ROM, VERY SHIT
######################
'''
ROM = []
firmware = [
"03",
"1205FF00FF",
".cpCPU: Wowtell 1025\n",
".acArchitecture: SSARIC Super Short and Rudimentary Instruction Set Computer\n",
".nl\n",
".mpNo ROM Loaded, Running Test\n",
".ifIf you see this, the if statement dont work\n",
".i2If you see this, the if statement for strings worked\n",
".w1test",
"02$cpr1",
"01",
"02$acr1",
"01",
"02$mpr1",
"01",
"0205r5",
"0205r6",
"05r1",
"01",
"06r1",
"01",
"07r1",
"01",
"08r1",
"01",
"02$nlr1",
"01",
".inTesting Input Function, Type Something And Press Enter\n] ",
"02$inr1",
"01",
"09$mp",
"02$mpr1",
"01",
"02$nlr1",
"01",
"0201r3",
"0202r4",
"0c0102",
"02$ifr1",
"01",
"10w101w102",
"02$i2r1",
"01",
"10w102w102",
"02$ifr1",
"01",
".cpArch",
"14$acac0004",
"10cp01ac02",
"1201050064",
"12015D0256",
"1364",
"03"
]

'''
#############
ROM EXECUTION
#############
'''
def run(ROM, firmware):
	ram_size = 32 # This is NOT in any size format, its in how many maximum entries
	val = {}
	if len(ROM)==0:
		ROM=firmware

	lineBeforeJump="00"
	i=0
	while i < len(ROM):
		line = ROM[i]
		if line[0]==".":
			if line[1]+line[2] not in registers:
				val[str(line[1]+line[2]).lower()]=line[3:]
			else:
				del val[line[1]+line[2]]
		elif line[0]!="-":
			inst=instructionset[line[0]+line[1]]
			print(inst*debug, end="")
			match inst:
				case "print":
					print(registers["r1"], end="")
				case "move": # Comment from 0.27: Kill me 
					if line[2] != "$":
						if str(line[4]) != "$":
							if str(line[4]+line[5]).lower() in registers:
								registers[str(line[4]+line[5]).lower()]=str(line[2]+line[3]).lower()
						else:
							if str(line[2]+line[3]).lower() in registers:
								val[str(line[5]+line[6])]=registers[str(line[2]+line[3]).lower()]
					else:
						if str(line[5]+line[6]).lower() in registers:
							registers[line[5]+line[6]]=val[str(line[3]+line[4]).lower()]
				case "clear":
					if os.name == "posix":
						os.system("clear")
					else:
						os.system("cls")
				case "jump":
					lineBeforeJump=str(hex(i))[2:]
					i=int(str(line[2]+line[3]), 16)-1
				case "back":
					i=lineBeforeJump-1
				case "mult":
					tmp_result=str(hex(int(registers["r5"], 16)*int(registers["r6"], 16)))[2:]
					if len(tmp_result) == 1:
						result="0"+tmp_result
					else:
						result=tmp_result
					if line[2] != "$":
						registers[str(line[2]+line[3]).lower()]=result
					else:
						val[str(line[3]+line[4]).lower()]=result
				case "divi":
					tmp_result=str(hex(round(int(registers["r5"], 16)/int(registers["r6"], 16))))[2:]
					if len(tmp_result) == 1:
						result="0"+tmp_result
					else:
						result=tmp_result
					if line[2] != "$":
						registers[str(line[2]+line[3]).lower()]=result
					else:
						val[str(line[3]+line[4]).lower()]=result
				case "addi":
					tmp_result=str(hex(int(registers["r5"], 16)+int(registers["r6"], 16)))[2:] # Fuck Floats
					if len(tmp_result) == 1:
						result="0"+tmp_result
					else:
						result=tmp_result
					if line[2] != "$":
						registers[str(line[2]+line[3]).lower()]=result
					else:
						val[str(line[3]+line[4]).lower()]=result
				case "subt":
					tmp_result=str(hex(int(registers["r5"], 16)-int(registers["r6"], 16)))[2:]
					if len(tmp_result) == 1:
						result="0"+tmp_result
					else:
						result=tmp_result
					if line[2] != "$":
						registers[str(line[2]+line[3]).lower()]=result
					else:
						val[str(line[3]+line[4]).lower()]=result
				case "input":
					inp=input()
					if line[2] != "$":
						if inp=="":
							inp="00"
						registers[str(line[2]+line[3]).lower()]=inp
					else:
						val[str(line[3]+line[4]).lower()]=inp
				case "delete":
					del val[line[2]+line[3]]
				case "if":
					hexToOperand = { # Made this cause im Lazy
					"01":"==",
					"02":"!=",
					"03":">=",
					"04":"<=",
					"05":">",
					"06":"<"
					}
					try:
						if eval(f"{'0x'+registers['r3']}{hexToOperand[line[2]+line[3]]}{'0x'+registers['r4']}"): # Top Ten Secure and not lazy code, definitly not sarcasm
							pass # this makes it continue normally
						else:
							i+=int(line[4]+line[5], 16)
					except:
						pass
				case "random":
					minimum=int(str(line[2]+line[3]), 16)
					maximum=int(str(line[4]+line[5]), 16)
					reg=str(line[6]+line[7])
					if reg in registers:
						randomNumber=str(hex(random.randint(minimum, maximum)))[2:]
						if len(randomNumber) == 1:
							registers[reg] = "0"+randomNumber
						else:
							registers[reg] = randomNumber
				case "add":
					if line[2] == "$":
						var1 = str(line[3]+line[4])
						var2 = str(line[6]+line[7])
						val[var2]+=val[var1]
					else:
						item1 = str(line[2]+line[3])
						var = str(line[5]+line[6])
						if item1 in registers:
							val[var] += str(registers[item1])
						else:
							val[var] += str(item1)
				case "modulo":
					tmp_result=str(hex(int(registers["r5"], 16)%int(registers["r6"], 16)))[2:]
					if len(tmp_result) == 1:
						result="0"+tmp_result
					else:
						result=tmp_result
					if line[2] != "$":
						registers[str(line[2]+line[3]).lower()]=result
					else:
						val[str(line[3]+line[4]).lower()]=result
				case "var_if":
					op1=str(line[2]+line[3])
					op2=str(line[6]+line[7])
					opr=str(line[4]+line[5])
					hexToOperand = { # Made this cause im Lazy
					"01":"==",
					"02":"!=",
					"03":">=",
					"04":"<=",
					"05":">",
					"06":"<"
					}
					try:
						if eval(f"'{val[op1]}'{hexToOperand[opr]}'{val[op2]}'") == True: # once again, very secure
							pass # this makes it continue normally
						else:
							i+=int(line[8]+line[9], 16)
					except:
						pass
				case "index":
					try:
						srcIsVar = 0
						if line[2] == "$":
							srcIsVar = 1
						else:
							srcIsVar = 0
						source = line[2+srcIsVar]+line[3+srcIsVar]
						destin = line[4+srcIsVar]+line[5+srcIsVar]
						index = line[6+srcIsVar]+line[7+srcIsVar]
						if srcIsVar == 1:
							if destin in registers:
								registers[destin] = val[source][int(index, 16)]
							elif destin in val:
								val[destin] = val[source][int(index, 16)]
						else:
							if destin in registers:
								registers[destin] = registers[source][int(index, 16)]
							elif destin in val:
								val[destin] = registers[source][int(index, 16)]
					except:
						pass
				case "beep":
					try:
						freq=int(line[2:6], 16) # i am NOT writing this out
						duration=int(line[6:10], 16) # neither am i NOT writing this out
						winsound.Beep(freq, duration)
					except:
						pass	
				case "sleep":
					time.sleep(int(line[2:9], 16)*0.01)
				case "index_range":
					try:
						srcIsVar = 0
						if line[2] == "$":
							srcIsVar = 1
						else:
							srcIsVar = 0
						source = line[2+srcIsVar]+line[3+srcIsVar]
						destin = line[4+srcIsVar]+line[5+srcIsVar]
						index_start = line[6+srcIsVar]+line[7+srcIsVar]
						index_end = line[8+srcIsVar]+line[9+srcIsVar]
						if srcIsVar == 1:
							if destin in registers:
								registers[destin] = val[source][int(index_start, 16):int(index_end, 16)]
							elif destin in val:
								val[destin] = val[source][int(index_start, 16):int(index_end, 16)]
						else:
							if destin in registers:
								registers[destin] = registers[source][int(index_start, 16):int(index_end, 16)]
							elif destin in val:
								val[destin] = registers[source][int(index_start, 16):int(index_end, 16)]
					except:
						pass
				case "fwrite":
				    file=val[line[2:4]]
				    content=val[line[4:6]]
				    with open(file, "w") as f:
				        f.write(content)
				case "fread":
				    file=val[line[2:4]]
				    content=line[4:6]
				    fline=int(line[6:9], 16])
				    with open(file, "r") as f:
				        lin=f.readlines()
				        val[content]=lin[fline]
				case "fcreate":
				    file=line[2:4]
				    with open(file, "x") as f:
				        pass
				case "fappend":
				    file=val[line[2:4]]
				    content=val[line[4:6]]
				    with open(file, "a") as f:
				        f.write(content)
				
		for register in registers.items():
			if len(register[1]) > rgstr_max_size:
				print(f"DATA OVERFLOW IN {register[0]}")
				quit()
		if len(val) > ram_size:
			print("TOO MANY ITEMS IN RAM")
			quit()
		i+=1

if __name__ == '__main__':
	run(ROM, firmware)
