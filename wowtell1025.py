# This is the first and probably worst CPU for PihOS, but this is the only CPU ill make for now
# Uhhh this is heavily inspired my the late Terry A. Davis (Allah Rahmet Eylesin)
# However unlike him I am bad at programming so im just gonna make this all virtual by just like this making a VCPU
# Also no optimizations for this. Its Currently 23:42 on a school night as im writing this. Im too tired. Fuck you
import os
import random

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
"r6":"00"
}
rgstr_max_size = 512

'''
#########################################################################
INSTRUCTION SET, VERY BAD, DO NOT TRY TO FIX, YOULL WANT TO DIE, TRUST ME
#########################################################################
'''
instructionset={
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
"0c":"if", # implemented
"0d":"random", # implemented
"0e":"add", # implemented
"0f":"modulo", # implemented
"10":"var_if" # implemented      # Also this is more for strings
} 

'''
######################
INBUILT ROM, VERY SHIT
######################
'''
ROM = []
firmware = [
"03",
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
"09r1",
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
"01"
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
			# print(inst, end="")
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
						os.system("clr")
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
					if inp == "":
						inp = "00"
					if line[2] != "$":
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
						if eval(f"'{val[op1]}'{hexToOperand[opr]}'{val[op2]}'"): # once again, very secure
							pass # this makes it continue normally
						else:
							i+=int(line[8]+line[9], 16)
					except:
						pass
					
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
