import re
#f = open('E:\\All Projects\\AssemblyConverter\\BeforeCompressAssembly.txt', 'r')
f = open('BeforeCompressAssembly.txt', 'r')
x = f.readlines()
f.close()

Pointer = []
Machine = []
Assembly = []

nochange = []

c = -1
for i in x:
        c += 1

        Ex1 = re.findall(' (\S+)\t', i)
        Pointer.append(Ex1)

        Ex2 = re.findall('\t(\S+)  ', i)
        Machine.append(Ex2)

        Ex3 = re.findall('\t(\S+)\t(\S+)\s', i)
        if Ex3 == [] and Ex1 != []:
                Ex3 = re.findall('\t([a-z]+)', i)
                Ex3 = [(Ex3[0], ' ')]
        Assembly.append(Ex3)
        if Ex1 == [] or Ex2 == [] or Ex3 == []:
                nochange.append(c)

for i in Pointer:
        if i == []:
                Pointer.remove(i)
                Machine.remove(i)
                Assembly.remove(i)
for i in range(len(Pointer)):
        Pointer[i] = Pointer[i][0]
        Machine[i] = Machine[i][0]
        Assembly[i] = Assembly[i][0][0]+' '+Assembly[i][0][1]


for index,i in enumerate(Assembly):
        if i == "nop  ":
                Assembly[index]="nop"
        elif i == "ret  ":
                Assembly[index] = "ret"
#print(Pointer)
PC = [4 for i in range(len(Assembly))]
# Read Stage Complete

"""***********************************************************************************************************"""

regKiList = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6",
             "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
regBits = {"s0": "000", "s1": "001", "a0": "010", "a1": "011", "a2": "100", "a3": "101", "a4": "110", "a5": "111"}
regList = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7",
           "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
regData={"s0":"000","s1":"001","a0":"010","a1":"011","a2":"100","a3":"101","a4":"110","a5":"111"}
regABI = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
inst={"add":["1001","00","00","10"] ,
          "sub":["1000","11","00","01"] ,
          "xor":["1000","11","01","01"] ,
          "or":["1000","11","10","01"] ,
          "and":["1000","11","11","01"] ,
          "mv":["1000","00","00","10"] ,
          "j":["101","00","00","01"] ,
          "jal":["001","00","00","01"] ,
          "jr":["1000","00","00","10"] ,
          "jalr":["1001","00","00","10"] ,
          "lw":["010","00","00","00"] ,
          "sw":["110","00","00","00"] ,
          "lwsp":["010","00","00","10"] ,
          "swsp":["110","00","00","10"] ,
          "addi":["000","00","00","01"] ,
          "andi":["100","10","00","01"] ,
          "beqz":["110","00","00","01"] ,
          "bnez":["111","00","00","01"] ,
          "nop":["0000","00000","00000","01"]}
"""******************************************Compressor Start*****************************************************************"""
def calculateUpwardLabel(label,instr):
    addr = 0
    for i in range(Pointer.index(label),Assembly.index(instr)):
        addr += PC[i]
    return -addr

def calculateLowerLabel(label,instr):
    addr = 0
    for j in range(Assembly.index(instr)+1,Pointer.index(label)+1):
        #addr += PC[i]
        i = Assembly[j]
        ex = i.split()
        if ex[0] != "bne" and ex[0] != "beq" and ex[0] != "j" and ex[0] != "jal":
            addr += PC[j]
        else:
            if ex[0] == "beq":
                regs = ex[1].split(",")
                # imd = regs[1]
                if regData.get(regs[0]) != None and regs[1] == "zero":
                    if Pointer.index(regs[2] + ":") < Assembly.index(i):
                        uu = calculateUpwardLabel(regs[2] + ":", i)
                    elif Pointer.index(regs[2] + ":") > Assembly.index(i):
                        uu = calculateLowerLabel(regs[2] + ":", i)
                    uu *= 2
                    # print(uu)
                    if -256 <= uu <= 254:
                        addr += 2
                    else:
                        addr += 4
            if ex[0] == "bne":
                regs = ex[1].split(",")
                # imd = regs[1]
                if regData.get(regs[0]) != None and regs[1] == "zero":
                    if Pointer.index(regs[2] + ":") < Assembly.index(i):
                        uu = calculateUpwardLabel(regs[2] + ":", i)
                    elif Pointer.index(regs[2] + ":") > Assembly.index(i):
                        uu = calculateLowerLabel(regs[2] + ":", i)
                    uu *= 2
                    #print(uu)
                    if -256 <= uu <= 254:
                        addr += 2
                    else:
                        addr += 4
            if ex[0] == "j":
                regs = ex[1].split(",")
                # imd = regs[1]
                if Pointer.index(regs[0] + ":") < Assembly.index(i):
                    uu = calculateUpwardLabel(regs[0] + ":", i)
                elif Pointer.index(regs[0] + ":") > Assembly.index(i):
                    uu = calculateLowerLabel(regs[0] + ":", i)
                uu *= 2
                #print(uu)
                if -2048 <= uu <= 2046:
                    addr += 2
                else:
                    addr += 4
            if ex[0] == "jal":
                regs = ex[1].split(",")
                # imd = regs[1]
                if regs[0] == "zero":
                    if Pointer.index(regs[1] + ":") < Assembly.index(i):
                        uu = calculateUpwardLabel(regs[1] + ":", i)
                    elif Pointer.index(regs[1] + ":") > Assembly.index(i):
                        uu = calculateLowerLabel(regs[1] + ":", i)
                    uu *= 2
                    #print(uu)
                    if -2048 <= uu <= 2046:
                        addr += 2
                    else:
                        addr += 4
                if regs[0] == "ra":
                    if Pointer.index(regs[1] + ":") < Assembly.index(i):
                        uu = calculateUpwardLabel(regs[1] + ":", i)
                    elif Pointer.index(regs[1] + ":") > Assembly.index(i):
                        uu = calculateLowerLabel(regs[1] + ":", i)
                    uu *= 2
                    #print(uu)
                    if -2048 <= uu <= 2046:
                        addr += 2
                    else:
                        addr += 4
    return addr

for index,i in enumerate(Assembly):
    k = i.split(" ")
    if k[0] == "li":
        regs = k[1].split(",")
        if regs[0] != regKiList[0] and regs[0] in regKiList and eval(regs[1]) <= 31 and eval(regs[1])>-32:
            imm = bin(eval(regs[1]))[2:].zfill(6)
            imm = str(imm)
            rd = bin(regKiList.index(regs[0]))[2:].zfill(5)
            binary = "010"+imm[0] + str(rd) + imm[1:] + "01"
            b = int(binary, 2)
            h = hex(b)
            h = str(h)
            h = h[2:]
            h = "0" * (4 - len(h)) + h
            Machine[index] = str(h)
            newInst = "c.li" + " " + k[1]
            Assembly[index] = newInst
            PC[index] = 2

    elif k[0] == "lui":
        regs = k[1].split(",")
        rd = bin(regKiList.index(regs[0]))[2:].zfill(5)
        machine = machineCode[index]
        binaryMachine = bin(int(machine, 16))[2:].zfill(32)
        binaryMachine = binaryMachine[:20]
        binaryMachine = str(binaryMachine)
        finalMAchine = binaryMachine
        if int(finalMAchine, 2) >= 1 and int(finalMAchine,2) <=63 :
            finalFinalMachine = finalMAchine[14:]
            binary = "011" + finalFinalMachine[0] + str(rd) + finalFinalMachine[1:6] + "01"
            b = int(binary, 2)
            h = hex(b)
            h = str(h)
            h = h[2:]
            h = "0" * (4 - len(h)) + h
            Machine[index] = str(h)
            newInst = "c.lui" + " " + k[1]
            Assembly[index] = newInst
            PC[index] = 2

    elif k[0] == "slli":
        regs = k[1].split(",")
        #print(regs)
        #print(int(regs[2], 16))
        if (regs[2])[0] == "-":
            if (regs[2])[1:3] == "0x":
                regs[2] = int(regs[2], 16)
            else:
                regs[2] = int(regs[2])
        else:
            if (regs[2])[0:2] == "0x":
                regs[2] = int(regs[2], 16)
            else:
                regs[2] = int(regs[2])


        if regs[0] != regKiList[0] and regs[1] != regKiList[0] and regs[2] > 0 and regs[2] <32 :
            #print(imm)
            regs[2] = str(regs[2])
            imm = bin(eval(regs[2]))[2:].zfill(6)
            imm = str(imm)
            #print(imm)
            if imm[0] == "0":
                rd = bin(regKiList.index(regs[0]))[2:].zfill(5)
                binary = "000" + imm[0] + str(rd) + imm[1:] + "10"
                b = int(binary, 2)
                h = hex(b)
                h = str(h)
                h = h[2:]
                h = "0" * (4 - len(h)) + h
                Machine[index] = str(h)
                newInst = "c.slli" + " " + regs[0]+","+regs[2]
                Assembly[index] = newInst
                PC[index] = 2

    elif k[0] == "srli":
        regs = k[1].split(",")
        if (regs[2])[0] == "-":
            if (regs[2])[1:3] == "0x":
                regs[2] = int(regs[2], 16)
            else:
                regs[2] = int(regs[2])
        else:
            if (regs[2])[0:2] == "0x":
                regs[2] = int(regs[2], 16)
            else:
                regs[2] = int(regs[2])
        if int(regs[2], 16) >0 and regs[0] in regBits and regs[1] in regBits and regs[0] == regs[1] and int(regs[2], 16) < 32:
            regs[2] = str(regs[2])
            imm = bin(eval(regs[2]))[2:].zfill(6)
            rd = regBits[regs[0]]
            binary = "100" + imm[0] + "00" + rd + imm[1:] + "01"
            #print(binary)
            b = int(binary, 2)
            h = hex(b)
            h = str(h)
            h = h[2:]
            h = "0" * (4 - len(h)) + h
            Machine[index] = str(h)
            newInst = "c.srli" + " " + k[1]
            Assembly[index] = newInst
            PC[index] = 2

    elif k[0] == "srai":
        regs = k[1].split(",")
        if (regs[2])[0] == "-":
            if (regs[2])[1:3] == "0x":
                regs[2] = int(regs[2], 16)
            else:
                regs[2] = int(regs[2])
        else:
            if (regs[2])[0:2] == "0x":
                regs[2] = int(regs[2], 16)
            else:
                regs[2] = int(regs[2])
        if int(regs[2], 16) >0 and regs[0] in regBits and regs[1] in regBits and regs[0] == regs[1] and int(regs[2], 16) < 32:
            regs[2] = str(regs[2])
            imm = bin(eval(regs[2]))[2:].zfill(6)
            rd = regBits[regs[0]]
            binary = "100" + imm[0] + "01" + rd + imm[1:] + "01"
            b = int(binary, 2)
            h = hex(b)
            h = str(h)
            h = h[2:]
            h = "0" * (4 - len(h)) + h
            Machine[index] = str(h)
            newInst = "c.srai" + " " + k[1]
            Assembly[index] = newInst
            PC[index] = 2

#for index, i in enumerate(Assembly):
    if i != "ret":
        if " " in i:
            ins, reg = i.split(" ")
            if ins == "add":
                rd, rs1, rs2 = reg.split(",")
                if rd != "zero" and rs2 != "zero" and rd == rs2:
                    rdBits, rs2Bits = bin(regList.index(rd))[2:].zfill(5), bin(regList.index(rs2))[2:].zfill(5)
                    bn = "1001" + str(rdBits) + str(rs2Bits) + "10"
                    b = int(bn, 2)
                    h = hex(b)
                    h = str(h)
                    h = h[2:]
                    h = "0" * (4 - len(h)) + h
                    rep = index
                    Assembly[rep] = "c.add" + " " + rd + "," + rs2
                    Machine[rep] = h
                    PC[index] = 2
            elif ins == "mv":
                rd, rs2 = reg.split(",")
                if rd != "zero" and rs2 != "zero":
                    rdBits, rs2Bits = bin(regList.index(rd))[2:].zfill(5), bin(regList.index(rs2))[2:].zfill(5)
                    bn = "1000" + str(rdBits) + str(rs2Bits) + "10"
                    b = int(bn, 2)
                    h = hex(b)
                    h = str(h)
                    h = h[2:]
                    h = "0" * (4 - len(h)) + h
                    Machine[index] = str(h)
                    newInst = "c.mv" + " " + rd + "," + rs2
                    Assembly[index] = newInst
                    PC[index] = 2

#for index, i in enumerate(Assembly):
    if " " in i:
        k,label = i.split(" ")
        if k == "addi":
            rd,rs1,imm = label.split(",")
            #------------------------------------------------------------ADDI16SP------------------------------------------
            if rd == "sp" and rs1 == "sp" and imm != "0":
                if eval(imm) < 2**6:
                    calcImm = eval(imm) * 16
                    if calcImm >= -512 and calcImm <=496:
                        bImm = bin(calcImm)[2:].zfill(6)
                        bImm = str(bImm)
                        binary = "011" + bImm[0] + str(bin(2)[2:].zfill(5)) + bImm[5] + bImm[3] + bImm[1] + bImm[2] + bImm[4] +"01"
                        b = int(binary, 2)
                        # print("b---", b)
                        h = hex(b)
                        h = str(h)
                        h = h[2:]
                        h = "0" * (4 - len(h)) + h
                        Machine[index] = str(h)
                        newInst = "c.addi16sp" + " " + str(int(bImm,2))
                        Assembly[index] = newInst
                        PC[index] = 2
            #---------------------------------------------------------------ADDI14SPN--------------------------------------
            elif rd in regBits.keys() and rs1 == "sp" and imm != "0":
                if eval(imm) < 2**8:
                    calcImm = eval(imm) * 4
                    if calcImm >= -512 and calcImm <= 508:
                        bImm = bin(calcImm)[2:].zfill(8)
                        bImm = str(bImm)
                        binary = "000" + bImm[4] + bImm[5] + bImm[0:4] + bImm[7] + bImm[6] + regBits[rd] + "00"
                        b = int(binary, 2)
                        # print("b---", b)
                        h = hex(b)
                        h = str(h)
                        h = h[2:]
                        h = "0" * (4 - len(h)) + h
                        Machine[index] = str(h)
                        newInst = "c.addi14spn" + " " + rd + "," + str(int(bImm,2))
                        Assembly[index] = newInst
                        PC[index] = 2

#for i in Assembly:
    ex=i.split()
    if ex[0] == "sub":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[2] and regs[0]!="zero":
                a=inst.get("sub")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep=Assembly.index(i)
                Assembly[rep]="c.sub"+" "+regs[0]+","+regs[2]
                Machine[rep]=f
                PC[index] = 2
    if ex[0] == "or":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[2] and regs[0]!="zero":
                a=inst.get("or")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep=Assembly.index(i)
                Assembly[rep]="c.or"+" "+regs[0]+","+regs[2]
                Machine[rep]=f
                PC[index] = 2
    if ex[0] == "xor":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[2] and regs[0]!="zero":
                a=inst.get("xor")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.xor" + " " + regs[0] + "," + regs[2]
                Machine[rep] = f
                PC[index] = 2
    if ex[0] == "and":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[2] and regs[0]!="zero":
                a=inst.get("and")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.and" + " " + regs[0] + "," + regs[2]
                Machine[rep] = f
                PC[index] = 2


    if ex[0] == "lw":
        imd = ((((ex[1]).split(","))[1]).split("("))[0]
        offset = ((ex[1].split(","))[1])[-3:-1]
        regs = ex[1].split(",")
        #imd = int(imd) / 4
        imd = str(int(imd)*4)
        if regData.get(regs[0]) != None and regData.get(offset) != None and int(imd) % 4 == 0 and 0 <= int(imd) <= 124:
            a = inst.get("lw")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            # print(b)
            imd = "0" * (7 - len(b)) + b
            imd = imd[::-1]
            # print(imd)
            final = a[0] + imd[5] + imd[4] + imd[3] + regData.get(offset) + imd[2] + imd[6] + regData.get(regs[0]) + a[
                3]
            b = hex(int(final, 2))
            f = b[2:]
            # print(imd,f)
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c."+i
            Machine[rep] = f
            PC[index] = 2

        if regs[0] != "zero" and offset == "sp" and 0 <= int(imd) <= 252 and int(imd) % 4 == 0:
            a = inst.get("lwsp")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            imd = "0" * (8 - len(b)) + b
            imd = imd[::-1]
            uu = regABI.index(regs[0])
            det = (str(bin(uu)))[2:]
            det = "0" * (5 - len(det)) + det
            final = a[0] + imd[5] + det + imd[4] + imd[3] + imd[2] + imd[7] + imd[6] + a[3]
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c." + i
            Machine[rep] = f
            PC[index] = 2

    if ex[0] == "sw":
        imd = ((((ex[1]).split(","))[1]).split("("))[0]
        offset = ((ex[1].split(","))[1])[-3:-1]
        regs = ex[1].split(",")
        #imd = int(imd) / 4
        imd = str(int(imd)*4)
        if regData.get(regs[0]) != None and regData.get(offset) != None and int(imd) % 4 == 0 and 0 <= int(imd) <= 124:
            #print(imd)
            a = inst.get("sw")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            #print(b)
            imd = "0" * (7 - len(b)) + b
            imd = imd[::-1]
            #print(imd)
            #print ("sw ki imd "+imd[6]+imd[5]+imd[4]+imd[3]+imd[2])
            final = a[0] + imd[5] + imd[4] + imd[3] + regData.get(offset) + imd[2] + imd[6] + regData.get(regs[0]) + a[
                3]
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c." + i
            Machine[rep] = f
            PC[index] = 2

        if offset == "sp" and 0 <= int(imd) <= 252 and int(imd) % 4 == 0:
            a = inst.get("swsp")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            imd = "0" * (8 - len(b)) + b
            imd = imd[::-1]
            uu = regABI.index(regs[0])
            det = (str(bin(uu)))[2:]
            det = "0" * (5 - len(det)) + det
            final = a[0] + imd[5] + imd[4] + imd[3] + imd[2] + imd[7] + imd[6] + det + a[3]
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c." + i
            Machine[rep] = f
            PC[index] = 2

    if ex[0] == "nop":
        rep = Assembly.index(i)
        Assembly[rep] = "c.nop"
        Machine[rep] = "0001"
        PC[index] = 2

    if ex[0] == "illegal":
        rep = Assembly.index(i)
        Assembly[rep] = "c.illegal"
        Machine[rep] = "0000"
        PC[index] = 2

    if ex[0] == "addi":
        regs = ex[1].split(",")
        imd = regs[2]
        if regs[0] == "zero" and regs[1] == "zero" and regs[2] == "0":
            rep = Assembly.index(i)
            Assembly[rep] = "c.nop"
            Machine[rep] = "0001"
            PC[index] = 2


    if ex[0] == "addi":
        regs = ex[1].split(",")
        imd = regs[2]
        if regs[0] != "zero" and regs[1] != "zero" and regs[0] == regs[1] and -32 <= int(imd) <= 31 and int(imd) != 0:
            #if regs[0] == regs[1]:
            a = inst.get("addi")
            uu = int(imd)
            if uu < 0:
                imd = ('{:0b}'.format(int(uu) & 0xffffffff))[-6:]
            else:
                imd = ('{:0b}'.format(int(uu) & 0xffffffff))
                imd = "0" * (6 - len(imd)) + imd
            #print(regData.get(regs[0]))
            uu = regABI.index(regs[0])
            det = (str(bin(uu)))[2:]
            det = "0" * (5 - len(det)) + det
            #print(imd,det)
            imd = imd[::-1]
            final = a[0] + imd[5] + det + imd[4] + imd[3] + imd[2] + imd[1] + imd[0] + a[3]
            #print(final)
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c.addi" + " " + regs[0] + "," + regs[2]
            Machine[rep] = f
            PC[index] = 2


    if ex[0] == "andi":
        regs=ex[1].split(",")
        imd=regs[2]
        #print(regs)
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regs[0] == regs[1] and -(2**6) < int(imd) < 2**6 :
            #if regs[0] == regs[1] :
            a = inst.get("andi")
            uu = int(imd)
            if uu < 0:
                imd = ('{:0b}'.format(int(uu) & 0xffffffff))[-6:]
            else:
                imd = ('{:0b}'.format(int(uu) & 0xffffffff))
                imd = "0" * (6 - len(imd)) + imd
            #print(imd)
            imd=imd[::-1]
            uu = regABI.index(regs[0])
            det = (str(bin(uu)))[2:]
            det = "0" * (5 - len(det)) + det
            det=det[-3::]
            final=a[0]+imd[5]+a[1]+det+imd[4]+imd[3]+imd[2]+imd[1]+imd[0]+a[3]
            b=hex(int(final,2))
            f=b[2:]
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c.andi" + " " + regs[0] + "," + regs[2]
            Machine[rep] = f
            PC[index] = 2

    if ex[0]=="jr":
        regs=ex[1].split(",")
        if regs[0] != "zero":
            uu = regABI.index(regs[0])
            det = (str(bin(uu)))[2:]
            det = "0" * (5 - len(det)) + det
            a=inst.get("jr")
            final=a[0]+det+"00000"+a[3]
            b=hex(int(final,2))
            f=b[2:]
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c.jr" + " " + regs[0]
            Machine[rep] = f
            PC[index] = 2


    if ex[0] =="jalr":
        regs=ex[1].split(",")
        #print(regs)
        #print(len(regs))
        if len(regs) == 1:
            if regs[0] != "zero":
                uu = regABI.index(regs[0])
                det = (str(bin(uu)))[2:]
                det = "0" * (5 - len(det)) + det
                a = inst.get("jalr")
                final = a[0] + det + "00000" + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.jalr" + " " + regs[0]
                Machine[rep] = f
                PC[index] = 2
        elif len(regs) == 3:
            #print(regs)
            if regs[0] == "ra" and regs[1] != "zero" and regs[2] == "0":
                print("done")
                uu = regABI.index(regs[1])
                det = (str(bin(uu)))[2:]
                det = "0" * (5 - len(det)) + det
                a = inst.get("jalr")
                final = a[0] + det + "00000" + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.jalr" + " " + regs[1]
                Machine[rep] = f
                PC[index] = 2
            elif regs[0] == "zero" and regs[1] != "zero" and regs[2] == "0":
                uu = regABI.index(regs[1])
                det = (str(bin(index)))[2:]
                det = "0" * (5 - len(det)) + det
                a = inst.get("jr")
                final = a[0] + det + "00000" + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.jr" + " " + regs[1]
                Machine[rep] = f
                PC[index] = 2


for index,i in enumerate(Assembly):
    ex = i.split()
    if ex[0] == "beq":
        regs = ex[1].split(",")
        # imd = regs[1]
        if regData.get(regs[0]) != None and regs[1] == "zero":
            if Pointer.index(regs[2]+":") < Assembly.index(i):
                uu = calculateUpwardLabel(regs[2]+":",i)
            elif Pointer.index(regs[2]+":") > Assembly.index(i):
                uu = calculateLowerLabel(regs[2] + ":", i)
            uu *= 2
            #print(uu)
            if -256 <= uu <= 254:
                a = inst.get("beqz")
                if uu < 0:
                    imd = ('{:0b}'.format(uu & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(uu & 0xffffffff))
                    imd = "0" * (11 - len(imd)) + imd
                # print(imd)
                imd = imd[::-1]
                #print(imd[::-1])
                final = a[0] + imd[8] + imd[4] + imd[3] + regData.get(regs[0]) + imd[7] + imd[6] + imd[2] + imd[1] + \
                        imd[
                            5] + a[3]
                # print(final)
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.beqz" + " " + regs[0]+","+regs[2]
                Machine[rep] = f
                PC[index] = 2
    if ex[0] == "bne":
        regs = ex[1].split(",")
        # imd = regs[1]
        if regData.get(regs[0]) != None and regs[1] == "zero":
            if Pointer.index(regs[2]+":") < Assembly.index(i):
                uu = calculateUpwardLabel(regs[2]+":",i)
            elif Pointer.index(regs[2]+":") > Assembly.index(i):
                uu = calculateLowerLabel(regs[2] + ":", i)
            uu *= 2
            #print(uu)
            if -256 <= uu <= 254:
                a = inst.get("bnez")
                if uu < 0:
                    imd = ('{:0b}'.format(uu & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(uu & 0xffffffff))
                    imd = "0" * (11 - len(imd)) + imd
                # print(imd)
                imd = imd[::-1]
                #print(imd[::-1])
                final = a[0] + imd[8] + imd[4] + imd[3] + regData.get(regs[0]) + imd[7] + imd[6] + imd[2] + imd[1] + \
                        imd[
                            5] + a[3]
                # print(final)
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.bnez" + " " + regs[0]+","+regs[2]
                Machine[rep] = f
                PC[index] = 2

    if ex[0] == "j":
        regs = ex[1].split(",")
        # imd = regs[1]
        if Pointer.index(regs[0] + ":") < Assembly.index(i):
            uu = calculateUpwardLabel(regs[0] + ":", i)
        elif Pointer.index(regs[0] + ":") > Assembly.index(i):
            uu = calculateLowerLabel(regs[0] + ":", i)
        uu *= 2
        #print(i,uu/2)
        if -2048 <= uu <= 2046:
            a = inst.get("j")
            if uu < 0:
                imd = ('{:0b}'.format(uu & 0xffffffff))[-11:]
            else:
                imd = ('{:0b}'.format(uu & 0xffffffff))
                imd = "0" * (12 - len(imd)) + imd
            # print(imd)
            imd = imd[::-1]
            # print(imd[::-1])
            final = a[0]+imd[11]+imd[4]+imd[9]+imd[8]+imd[10]+imd[6]+imd[7]+imd[3]+imd[2]+imd[1]+imd[5]+a[3]
            # print(final)
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = Assembly.index(i)
            Assembly[rep] = "c.j" + " " + regs[0]
            Machine[rep] = f
            PC[index] = 2

    if ex[0] == "jal":
        regs = ex[1].split(",")
        # imd = regs[1]
        if regs[0] == "zero":
            if Pointer.index(regs[1] + ":") < Assembly.index(i):
                uu = calculateUpwardLabel(regs[1] + ":", i)
            elif Pointer.index(regs[1] + ":") > Assembly.index(i):
                uu = calculateLowerLabel(regs[1] + ":", i)
            uu *= 2
            #print(uu)
            if -2048 <= uu <= 2046:
                a = inst.get("j")
                if uu < 0:
                    imd = ('{:0b}'.format(uu & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(uu & 0xffffffff))
                    imd = "0" * (12 - len(imd)) + imd
                # print(imd)
                imd = imd[::-1]
                # print(imd[::-1])
                final = a[0]+imd[11]+imd[4]+imd[9]+imd[8]+imd[10]+imd[6]+imd[7]+imd[3]+imd[2]+imd[1]+imd[5]+a[3]
                # print(final)
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.j" + " " + regs[1]
                Machine[rep] = f
                PC[index] = 2
        if regs[0] == "ra":
            if Pointer.index(regs[1] + ":") < Assembly.index(i):
                uu = calculateUpwardLabel(regs[1] + ":", i)
            elif Pointer.index(regs[1] + ":") > Assembly.index(i):
                uu = calculateLowerLabel(regs[1] + ":", i)
            uu *= 2
            #print(uu)
            if -2048 <= uu <= 2046:
                a = inst.get("jal")
                if uu < 0:
                    imd = ('{:0b}'.format(uu & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(uu & 0xffffffff))
                    imd = "0" * (12 - len(imd)) + imd
                # print(imd)
                imd = imd[::-1]
                # print(imd[::-1])
                final = a[0]+imd[11]+imd[4]+imd[9]+imd[8]+imd[10]+imd[6]+imd[7]+imd[3]+imd[2]+imd[1]+imd[5]+a[3]
                # print(final)
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = Assembly.index(i)
                Assembly[rep] = "c.jal" + " " + regs[1]
                Machine[rep] = f
                PC[index] = 2

"""^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^Calculating total no. of instructions.^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"""
#print("Distance from Instruction to Label",calculateLowerLabel("10274:","c.j 10274"))
#print(PC.count(2))
count = 0
for i in Assembly:
    if i[0:2] == "c.":
        count +=1
print("Total compressed instructions are:",count)
"""******************************************Compressor End*****************************************************************"""
#file3=open("E:\\All Projects\\AssemblyConverter\\Machine_Code.txt","w")
file3=open("Machine_Code.txt","w")
for i in Machine:
    file3.write(i+"\n")
file3.close()
# Write Stage Begins
#f = open('E:\\All Projects\\AssemblyConverter\\new.txt', "w")
f = open('new.txt', "w")
counter = -1
skipped = 0
#print(Assembly)
while True:
        counter += 1
        if counter in nochange:
                skipped += 1
                f.write(x[counter])
        else:
                index = counter-skipped
                try:
                        if len(Machine[index]) == 8:
                                f.write(str(Pointer[index])+'          '+str(Machine[index])+'          '+str(Assembly[index])+'\n')
                        else:
                                f.write(str(Pointer[index])+'          '+str(Machine[index])+'              '+str(Assembly[index])+'\n')
                except:
                        break
f.close()



