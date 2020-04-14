import bitstring
f = open("assembly.txt", "r")
l = f.readlines()
f.close()
#print(l)

for i in l:
    if i == "\n":
        ind = l.index(i)
        m = l[:ind]
        l = l[ind+1:]
        break
#print(l
#)
instruction = []
mainInstruction = []
machineCode = []
#print(m)

for i in m:
    i = i[:-1]
    machineCode.append(i)

#print(machineCode)

for i in l:
    i = i[:-1]
    mainInstruction.append(i)
#print(instruction)
for i in mainInstruction:
    if " " in i:
        instruction.append(i)

#print(instruction.index("up:"))

regKiList = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6",
             "a7", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
regBits = {"s0": "000", "s1": "001", "a0": "010", "a1": "011", "a2": "100", "a3": "101", "a4": "110", "a5": "111"}
regList = ["zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2", "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7",
           "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6"]
for index, i in enumerate(instruction):
    if i != "ret":
        if " " in i:
            #print(i)
            ins, reg = i.split(" ")
            if ins == "add":
                rd, rs1, rs2 = reg.split(",")
                # print(rd,rs1,rs2)
                if rd != "zero" and rs2 != "zero" and rd == rs1:
                    #print(ins, rd, rs1, rs2)
                    # print(reg.index(rd))
                    rdBits, rs2Bits = bin(regList.index(rd))[2:].zfill(5), bin(regList.index(rs2))[2:].zfill(5)
                    # print(rdBits, rs2Bits)
                    bn = "1001" + str(rdBits) + str(rs2Bits) + "10"
                    #print(bn)
                    # print(len(bn))
                    b = int(bn, 2)
                    # print("b---", b)
                    h = hex(b)
                    h = str(h)
                    h = h[2:]
                    machineCode[index] = str(h)

                    newInst = "c.add" + "\t" + rd + "," + rs2
                    # print(newInst)

                    instruction[index] = "\t" + newInst

                # elif rd != "zero" and rs2 != "zero" and rs1 == "zero":
                #     rdBits, rs2Bits = bin(regList.index(rd))[2:].zfill(5), bin(regList.index(rs2))[2:].zfill(5)
                #     # print(rdBits, rs2Bits)
                #     bn = "1000" + str(rdBits) + str(rs2Bits) + "10"
                #     # print(bn)
                #     # print(len(bn))
                #     b = int(bn, 2)
                #     # print("b---", b)
                #     h = hex(b)
                #     h = str(h)
                #     h = h[2:]
                #     machineCode[index] = str(h)
                #
                #     newInst = "c.mv" + "\t" + rd + "," + rs2
                #     # print(newInst)
                #
                #     instruction[index] = "\t" + newInst
            elif ins == "mv":
                rd, rs2 = reg.split(",")
                if rd != "zero" and rs2 != "zero":
                    rdBits, rs2Bits = bin(regList.index(rd))[2:].zfill(5), bin(regList.index(rs2))[2:].zfill(5)
                    # print(rdBits, rs2Bits)
                    bn = "1000" + str(rdBits) + str(rs2Bits) + "10"
                    # print(bn)
                    # print(len(bn))
                    b = int(bn, 2)
                    # print("b---", b)
                    h = hex(b)
                    h = str(h)
                    h = h[2:]
                    machineCode[index] = str(h)

                    newInst = "c.mv" + "\t" + rd + "," + rs2
                    instruction[index] = "\t" + newInst

#---------------------Ch3king-Instructions------------------------
for i,inst in enumerate(instruction):
    inst = inst.split(" ")
    #print(i,inst)

#-----------------------li-instruction--------------------------
    if inst[0] == "li":
        regs = inst[1].split(",")
        if regs[0] != regKiList[0] and regs[0] in regKiList and eval(regs[1]) <= 31 and eval(regs[1])>-32:
            print("Hello", i)
            print(machineCode[i])
            imm = bin(eval(regs[1]))[2:].zfill(6)
            imm = str(imm)
            print("imm",imm)
            #print(imm)
            rd = bin(regKiList.index(regs[0]))[2:].zfill(5)
            #print(rd)

            binary = "010"+imm[0] + str(rd) + imm[1:] + "01"
            print(binary)
            #print("binary--", binary)
            b = int(binary, 2)
            #print("b---", b)
            h = hex(b)
            h = str(h)
            h = h[2:]
            print(h)
            machineCode[i] = str(h)

            newInst = "c.li" +"\t"+ inst[1]
           # print(newInst)

            instruction[i] = "\t" + newInst


#---------------------lui-instruction------------------------  -32 <-> 31 right-6
    elif inst[0] == "lui":
        regs = inst[1].split(",")
        rd = bin(regKiList.index(regs[0]))[2:].zfill(5)
        machine = machineCode[i]

        binaryMachine = bin(int(machine, 16))[2:].zfill(32)
        binaryMachine = binaryMachine[:20]
        binaryMachine = str(binaryMachine)
        finalMAchine = binaryMachine


        if int(finalMAchine, 2) >= 1 and int(finalMAchine,2) <=63 :
            finalFinalMachine = finalMAchine[14:]
            binary = "011" + finalFinalMachine[0] + str(rd) + finalFinalMachine[1:6] + "01"
            b = int(binary, 2)
            # print("b---", b)
            h = hex(b)
            h = str(h)
            h = h[2:]
            machineCode[i] = str(h)

            newInst = "c.lui" + "\t" + inst[1]
            # print(newInst)

            instruction[i] = "\t" + newInst



        # if regs[1] != "0" and (regs[0] !=  regKiList[0] and regs[0] != regKiList[2]):
        #     imm = bin(eval(regs[1]))[2:].zfill(17)
        #     if imm != bin(0)[2:].zfill(17):
        #         imm = str(imm)
        #
        #
        #         binary = "011" + imm[0] + str(rd) + imm[1:6] + "01"




#--------------------slli-instruction-------------------------
    elif inst[0] == "slli":
        regs = inst[1].split(",")
        #print(regs)
        #print(regKiList.index("a5"))
        if regs[0] != regKiList[0] and regs[1] != regKiList[0] and eval(regs[2]) > 0 and eval(regs[2]) <32 :
            #print(regs[2][2])
            imm = bin(eval(regs[2]))[2:].zfill(6)
            #if imm < bin(32)[2:].zfill(6):
            imm = str(imm)
            #print(imm)
            #print(imm[0] == "0")
            if imm[0] == "0":
                rd = bin(regKiList.index(regs[0]))[2:].zfill(5)
                #print(rd)
                binary = "000" + imm[0] + str(rd) + imm[1:] + "10"
                #print(len(str(binary)))
                #print(binary)
                b = int(binary, 2)
                #print(b)
                #print("b---", b)
                h = hex(b)
                h = str(h)
                h = h[2:]
                machineCode[i] = str(h)

                newInst = "c.slli" + "\t" + inst[1]
                #print(newInst)

                instruction[i] = "\t" + newInst


#-----------------------srli---instruction-----------------------------
    elif inst[0] == "srli":
        regs = inst[1].split(",")
        if eval(regs[2]) >0 and regs[0] in regBits and regs[1] in regBits and regs[0] == regs[1] and eval(regs[2]) < 32:
            #rd = bin(reg.index(regs[0]))[2:].zfill(5)
            imm = bin(eval(regs[2]))[2:].zfill(6)

            rd = regBits[regs[0]]
            binary = "100" + imm[0] + "00" + rd + imm[1:] + "01"
            print(binary)
            b = int(binary, 2)
            # print("b---", b)
            h = hex(b)
            h = str(h)
            h = h[2:]
            machineCode[i] = str(h)

            newInst = "c.srli" + "\t" + inst[1]
            # print(newInst)

            instruction[i] = "\t" + newInst


#---------------------srai--instruction------------------------------
    elif inst[0] == "srai":
        regs = inst[1].split(",")
        if eval(regs[2]) >0 and regs[0] in regBits and regs[1] in regBits and regs[0] == regs[1] and eval(regs[2]) < 32:
            # rd = bin(reg.index(regs[0]))[2:].zfill(5)
            imm = bin(eval(regs[2]))[2:].zfill(6)

            rd = regBits[regs[0]]
            binary = "100" + imm[0] + "01" + rd + imm[1:] + "01"
            b = int(binary, 2)
            # print("b---", b)
            h = hex(b)
            h = str(h)
            h = h[2:]
            machineCode[i] = str(h)

            newInst = "c.srai" + "\t" + inst[1]
            # print(newInst)

            instruction[i] = "\t" + newInst

for index, inst in enumerate(instruction):
    #print(inst)
    if " " in inst:
        i,label = inst.split(" ")
        if i == "j":
            # machine = machineCode[index]
            # binaryMachine = bin(int(machine, 16))[2:].zfill(32)
            # binaryMachine = binaryMachine[:20]
            # binaryMachine = str(binaryMachine)
            # finalMAchine = binaryMachine[0] + binaryMachine[10:] + binaryMachine[9] + binaryMachine[1:9]
            #
            # if int(finalMAchine, 2) >= -2048 and int(finalMAchine, 2) <= 2046:
            #     finalFinalMachine = finalMAchine[9:]
            #     pmb = finalFinalMachine
            #     binary = "101" + pmb[0] + pmb[7] + pmb[2] + pmb[3] + pmb[1] + pmb[5] + pmb[4] + pmb[8] + pmb[9] + pmb[10] + pmb[6] + "01"
            #
            #     b = int(binary, 2)
            #     # print("b---", b)
            #     h = hex(b)
            #     h = str(h)
            #     h = h[2:]
            #     machineCode[index] = str(h)
            #
            #     newInst = "c.j" + "\t" + label
            #     # print(newInst)
            #
            #     instruction[index] = "\t" + newInst

            machine = machineCode[index]
            binaryMachine = bin(int(machine, 16))[2:].zfill(32)
            # print("32-bit Binary---",binaryMachine)
            binaryMachine = binaryMachine[:20]
            # print("unarange 20-bit =----", binaryMachine)
            binaryMachine = str(binaryMachine)
            # binaryMachine=binaryMachine[::-1]
            # binaryMachine = "0"+ binaryMachine
            # print(binaryMachine)
            # bit20 = binaryMachine[1:11]
            # print("20th--",bit20)
            # bit10_1 = binaryMachine[1:11]
            # bit10_1 = bit10_1[::-1]
            # print("1-10---", bit10_1)
            # bit11 = binaryMachine[11]
            # print("11--", bit11)
            # bit19_12 = binaryMachine[12:20]
            # bit19_12 = bit19_12[::-1]
            # print("19-20--", bit19_12)
            # print("---", binaryMachine[2:11])
            # a = binaryMachine[2:11]
            a = binaryMachine[1:11]
            b = binaryMachine[11]
            c = binaryMachine[12:20]
            d = binaryMachine[0]
            finalMAchine = "0b" + d + c + b + a

            import bitstring

            aaa = bitstring.BitArray(finalMAchine)
            # print(";;;------;;",aaa.int)
            #
            # print("HEX---", machine)
            # print("binary of Imm---", finalMAchine)
            # print("decimal of Imm---", int(finalMAchine, 2))
            finalFinalMachine = finalMAchine[9:]
            # print("11-bit bianry---", finalFinalMachine)

            if aaa.int >= -2048 and aaa.int <= 2046:
                finalFinalMachine = finalMAchine[9:]
                # print("11-bit bianry---", finalFinalMachine)
                pmb = finalFinalMachine
                binary = "101" + pmb[0] + pmb[7] + pmb[2] + pmb[3] + pmb[1] + pmb[5] + pmb[4] + pmb[8] + pmb[9] + pmb[
                    10] + pmb[6] + "01"

                b = int(binary, 2)
                # print("b---", b)
                h = hex(b)
                h = str(h)
                h = h[2:]
                machineCode[index] = str(h)

                newInst = "c.j" + "\t" + label
                # print(newInst)

                instruction[index] = "\t" + newInst

        elif i == "jal":
            if "," not in label:
                machine = machineCode[index]
                binaryMachine = bin(int(machine, 16))[2:].zfill(32)
                #print("32-bit Binary---",binaryMachine)
                binaryMachine = binaryMachine[:20]
                #print("unarange 20-bit =----", binaryMachine)
                binaryMachine = str(binaryMachine)
                #binaryMachine=binaryMachine[::-1]
                #binaryMachine = "0"+ binaryMachine
                #print(binaryMachine)
                # bit20 = binaryMachine[1:11]
                # print("20th--",bit20)
                # bit10_1 = binaryMachine[1:11]
                # bit10_1 = bit10_1[::-1]
                # print("1-10---", bit10_1)
                # bit11 = binaryMachine[11]
                # print("11--", bit11)
                # bit19_12 = binaryMachine[12:20]
                # bit19_12 = bit19_12[::-1]
                # print("19-20--", bit19_12)
                # print("---", binaryMachine[2:11])
                # a = binaryMachine[2:11]
                a = binaryMachine[1:11]
                b = binaryMachine[11]
                c = binaryMachine[12:20]
                d = binaryMachine[0]
                finalMAchine = "0b"+d+c+b+a

                import bitstring

                aaa = bitstring.BitArray(finalMAchine)
                # print(";;;------;;",aaa.int)
                #
                # print("HEX---", machine)
                # print("binary of Imm---", finalMAchine)
                # print("decimal of Imm---", int(finalMAchine, 2))
                finalFinalMachine = finalMAchine[9:]
                #print("11-bit bianry---", finalFinalMachine)


                if aaa.int >= -2048 and aaa.int <= 2046:
                    finalFinalMachine = finalMAchine[9:]
                    #print("11-bit bianry---", finalFinalMachine)
                    pmb = finalFinalMachine
                    binary = "001" + pmb[0] + pmb[7] + pmb[2] + pmb[3] + pmb[1] + pmb[5] + pmb[4] + pmb[8] + pmb[9] + pmb[10] + pmb[6] + "01"

                    b = int(binary, 2)
                    # print("b---", b)
                    h = hex(b)
                    h = str(h)
                    h = h[2:]
                    machineCode[index] = str(h)

                    newInst = "c.jal" + "\t" + label
                    # print(newInst)

                    instruction[index] = "\t" + newInst


            else:
                reg,lb = label.split(",")
                if reg == "zero":
                    # machine = machineCode[index]
                    # binaryMachine = bin(int(machine, 16))[2:].zfill(32)
                    # binaryMachine = binaryMachine[:20]
                    # binaryMachine = str(binaryMachine)
                    # finalMAchine = binaryMachine[0] + binaryMachine[10:] + binaryMachine[9] + binaryMachine[1:9]
                    #
                    # if int(finalMAchine, 2) >= -2048 and int(finalMAchine, 2) <= 2046:
                    #     finalFinalMachine = finalMAchine[9:]
                    #     pmb = finalFinalMachine
                    #     binary = "101" + pmb[0] + pmb[7] + pmb[2] + pmb[3] + pmb[1] + pmb[5] + pmb[4] + pmb[8] + pmb[9] + pmb[10] + pmb[6] + "01"
                    #
                    #     b = int(binary, 2)
                    #     # print("b---", b)
                    #     h = hex(b)
                    #     h = str(h)
                    #     h = h[2:]
                    #     machineCode[index] = str(h)
                    #
                    #     newInst = "c.j" + "\t" + label
                    #     # print(newInst)
                    #
                    #     instruction[index] = "\t" + newInst
                    machine = machineCode[index]
                    binaryMachine = bin(int(machine, 16))[2:].zfill(32)
                    # print("32-bit Binary---",binaryMachine)
                    binaryMachine = binaryMachine[:20]
                    # print("unarange 20-bit =----", binaryMachine)
                    binaryMachine = str(binaryMachine)
                    # binaryMachine=binaryMachine[::-1]
                    # binaryMachine = "0"+ binaryMachine
                    # print(binaryMachine)
                    # bit20 = binaryMachine[1:11]
                    # print("20th--",bit20)
                    # bit10_1 = binaryMachine[1:11]
                    # bit10_1 = bit10_1[::-1]
                    # print("1-10---", bit10_1)
                    # bit11 = binaryMachine[11]
                    # print("11--", bit11)
                    # bit19_12 = binaryMachine[12:20]
                    # bit19_12 = bit19_12[::-1]
                    # print("19-20--", bit19_12)
                    # print("---", binaryMachine[2:11])
                    # a = binaryMachine[2:11]
                    a = binaryMachine[1:11]
                    b = binaryMachine[11]
                    c = binaryMachine[12:20]
                    d = binaryMachine[0]
                    finalMAchine = "0b" + d + c + b + a

                    import bitstring

                    aaa = bitstring.BitArray(finalMAchine)
                    # print(";;;------;;",aaa.int)
                    #
                    # print("HEX---", machine)
                    # print("binary of Imm---", finalMAchine)
                    # print("decimal of Imm---", int(finalMAchine, 2))
                    finalFinalMachine = finalMAchine[9:]
                    # print("11-bit bianry---", finalFinalMachine)

                    if aaa.int >= -2048 and aaa.int <= 2046:
                        finalFinalMachine = finalMAchine[9:]
                        # print("11-bit bianry---", finalFinalMachine)
                        pmb = finalFinalMachine
                        binary = "101" + pmb[0] + pmb[7] + pmb[2] + pmb[3] + pmb[1] + pmb[5] + pmb[4] + pmb[8] + pmb[
                            9] + pmb[10] + pmb[6] + "01"

                        b = int(binary, 2)
                        # print("b---", b)
                        h = hex(b)
                        h = str(h)
                        h = h[2:]
                        machineCode[index] = str(h)

                        newInst = "c.j" + "\t" + label
                        # print(newInst)

                        instruction[index] = "\t" + newInst

                elif reg == "ra":
                    # machine = machineCode[index]
                    # binaryMachine = bin(int(machine, 16))[2:].zfill(32)
                    # binaryMachine = binaryMachine[:20]
                    # binaryMachine = str(binaryMachine)
                    # finalMAchine = binaryMachine[0] + binaryMachine[10:] + binaryMachine[9] + binaryMachine[1:9]
                    #
                    # if int(finalMAchine, 2) >= -2048 and int(finalMAchine, 2) <= 2046:
                    #     finalFinalMachine = finalMAchine[9:]
                    #     pmb = finalFinalMachine
                    #     binary = "001" + pmb[0] + pmb[7] + pmb[2] + pmb[3] + pmb[1] + pmb[5] + pmb[4] + pmb[8] + pmb[9] + pmb[10] + pmb[6] + "01"
                    #
                    #     b = int(binary, 2)
                    #     # print("b---", b)
                    #     h = hex(b)
                    #     h = str(h)
                    #     h = h[2:]
                    #     machineCode[index] = str(h)
                    #
                    #     newInst = "c.jal" + "\t" + label
                    #     # print(newInst)
                    #
                    #     instruction[index] = "\t" + newInst
                    machine = machineCode[index]
                    binaryMachine = bin(int(machine, 16))[2:].zfill(32)
                    # print("32-bit Binary---",binaryMachine)
                    binaryMachine = binaryMachine[:20]
                    # print("unarange 20-bit =----", binaryMachine)
                    binaryMachine = str(binaryMachine)
                    # binaryMachine=binaryMachine[::-1]
                    # binaryMachine = "0"+ binaryMachine
                    # print(binaryMachine)
                    # bit20 = binaryMachine[1:11]
                    # print("20th--",bit20)
                    # bit10_1 = binaryMachine[1:11]
                    # bit10_1 = bit10_1[::-1]
                    # print("1-10---", bit10_1)
                    # bit11 = binaryMachine[11]
                    # print("11--", bit11)
                    # bit19_12 = binaryMachine[12:20]
                    # bit19_12 = bit19_12[::-1]
                    # print("19-20--", bit19_12)
                    # print("---", binaryMachine[2:11])
                    # a = binaryMachine[2:11]
                    a = binaryMachine[1:11]
                    b = binaryMachine[11]
                    c = binaryMachine[12:20]
                    d = binaryMachine[0]
                    finalMAchine = "0b" + d + c + b + a

                    import bitstring

                    aaa = bitstring.BitArray(finalMAchine)
                    # print(";;;------;;",aaa.int)
                    #
                    # print("HEX---", machine)
                    # print("binary of Imm---", finalMAchine)
                    # print("decimal of Imm---", int(finalMAchine, 2))
                    finalFinalMachine = finalMAchine[9:]
                    # print("11-bit bianry---", finalFinalMachine)

                    if aaa.int >= -2048 and aaa.int <= 2046:
                        finalFinalMachine = finalMAchine[9:]
                        # print("11-bit bianry---", finalFinalMachine)
                        pmb = finalFinalMachine
                        binary = "001" + pmb[0] + pmb[7] + pmb[2] + pmb[3] + pmb[1] + pmb[5] + pmb[4] + pmb[8] + pmb[
                            9] + pmb[10] + pmb[6] + "01"

                        b = int(binary, 2)
                        # print("b---", b)
                        h = hex(b)
                        h = str(h)
                        h = h[2:]
                        machineCode[index] = str(h)

                        newInst = "c.jal" + "\t" + label
                        # print(newInst)

                        instruction[index] = "\t" + newInst



        elif i == "addi":
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
                        machineCode[index] = str(h)

                        newInst = "c.addi16sp" + "\t" + str(bImm)
                        # print(newInst)

                        instruction[index] = "\t" + newInst
            #---------------------------------------------------------------ADDI4SPN--------------------------------------
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
                        machineCode[index] = str(h)

                        newInst = "c.addi4spn" + "\t" + rd + str(bImm)
                        # print(newInst)

                        instruction[index] = "\t" + newInst




#----------------------------------------------------------------patches------------------------------
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
file=open("C:\\Users\\hafiz\\Desktop\\newFormatMachineCode.txt","r")
data=file.readlines()
machine=[]
assembly=[]
raw=[]
file.close()
a=data.index("\n")
for i in range(a):
    machine.append((data[i])[:-1])
labels=0
for i in range(a+1,len(data)):
    if (data[i])[-2] != ":":
        if data[i][-1] == "\n":
            assembly.append((data[i])[:-1])
            raw.append((data[i])[:-1])
        else:
            assembly.append(data[i])
            raw.append(data[i])
    else:
        if data[i][-1] == "\n":
            raw.append((data[i])[:-1])
        else:
            raw.append(data[i])
        labels+=1

for i in assembly:
    ex=i.split()
    if ex[0] == "sub":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[1] and regs[0]!="zero":
                a=inst.get("sub")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep=assembly.index(i)
                #assembly[rep]="c.sub"+" "+regs[0]+","+regs[2]
                machine[rep]=f
    if ex[0] == "or":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[1] and regs[0]!="zero":
                a=inst.get("or")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep=assembly.index(i)
                #assembly[rep]="c.sub"+" "+regs[0]+","+regs[2]
                machine[rep]=f
    if ex[0] == "xor":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[1] and regs[0]!="zero":
                a=inst.get("xor")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep=assembly.index(i)
                #assembly[rep]="c.sub"+" "+regs[0]+","+regs[2]
                machine[rep]=f
    if ex[0] == "and":
        regs=ex[1].split(",")
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regData.get(regs[2])!= None :
            if regs[0] == regs[1] and regs[0]!="zero":
                a=inst.get("and")
                final=a[0]+a[1]+regData.get(regs[0])+a[2]+regData.get(regs[2])+a[3]
                b=hex(int(final,2))
                f=b[2:]
                f = "0" * (4 - len(f)) + f
                rep=assembly.index(i)
                #assembly[rep]="c.sub"+" "+regs[0]+","+regs[2]
                machine[rep]=f

    if ex[0] == "lw":
        imd = ((((ex[1]).split(","))[1]).split("("))[0]
        offset = ((ex[1].split(","))[1])[-3:-1]
        regs = ex[1].split(",")
        #imd = int(imd) / 4
        imd = str(int(imd))
        if regData.get(regs[0]) != None and regData.get(offset) != None and int(imd) % 4 == 0 and 0 <= int(imd) <= 252:
            a = inst.get("lw")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            # print(b)
            imd = "0" * (8 - len(b)) + b
            imd = imd[::-1]
            # print(imd)
            final = a[0] + imd[5] + imd[4] + imd[3] + regData.get(offset) + imd[2] + imd[6] + regData.get(regs[0]) + a[
                3]
            b = hex(int(final, 2))
            f = b[2:]
            # print(imd,f)
            f = "0" * (4 - len(f)) + f
            rep = assembly.index(i)
            machine[rep] = f

        if regs[0] != "zero" and offset == "sp" and 0 <= int(imd) <= 252 and int(imd) % 4 == 0:
            a = inst.get("lwsp")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            imd = "0" * (8 - len(b)) + b
            imd = imd[::-1]
            index = regABI.index(regs[0])
            det = (str(bin(index)))[2:]
            det = "0" * (5 - len(det)) + det
            final = a[0] + imd[5] + det + imd[4] + imd[3] + imd[2] + imd[7] + imd[6] + a[3]
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = assembly.index(i)
            machine[rep] = f

    if ex[0] == "sw":
        imd = ((((ex[1]).split(","))[1]).split("("))[0]
        offset = ((ex[1].split(","))[1])[-3:-1]
        regs = ex[1].split(",")
        #imd = int(imd) / 4
        imd = str(int(imd))
        if regData.get(regs[0]) != None and regData.get(offset) != None and int(imd) % 4 == 0 and 0 <= int(imd) <= 252:
            # print(imd)
            a = inst.get("sw")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            imd = "0" * (8 - len(b)) + b
            imd = imd[::-1]
            final = a[0] + imd[5] + imd[4] + imd[3] + regData.get(offset) + imd[2] + imd[6] + regData.get(regs[0]) + a[
                3]
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = assembly.index(i)
            machine[rep] = f

        if offset == "sp" and 0 <= int(imd) <= 252 and int(imd) % 4 == 0:
            a = inst.get("swsp")
            b = (bin(int(imd)))  # [2:]
            if (str(b))[0] == "-":
                b = b[3:]
            else:
                b = b[2:]
            imd = "0" * (8 - len(b)) + b
            imd = imd[::-1]
            index = regABI.index(regs[0])
            det = (str(bin(index)))[2:]
            det = "0" * (5 - len(det)) + det
            final = a[0] + imd[5] + imd[4] + imd[3] + imd[2] + imd[7] + imd[6] + det + a[3]
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = assembly.index(i)
            machine[rep] = f

    if ex[0] == "addi":
        regs = ex[1].split(",")
        imd = regs[2]
        if regs[0] != "zero" and regs[0] != "zero" and regs[0] == regs[1] and -32 <= int(imd) <= 31 and int(imd) != 0:
            #if regs[0] == regs[1]:
            a = inst.get("addi")
            index = int(imd)
            if index < 0:
                imd = ('{:0b}'.format(int(index) & 0xffffffff))[-6:]
            else:
                imd = ('{:0b}'.format(int(index) & 0xffffffff))
                imd = "0" * (6 - len(imd)) + imd
            #print(regData.get(regs[0]))
            index = regABI.index(regs[0])
            det = (str(bin(index)))[2:]
            det = "0" * (5 - len(det)) + det
            #print(imd,det)
            imd = imd[::-1]
            final = a[0] + imd[5] + det + imd[4] + imd[3] + imd[2] + imd[1] + imd[0] + a[3]
            #print(final)
            b = hex(int(final, 2))
            f = b[2:]
            f = "0" * (4 - len(f)) + f
            rep = assembly.index(i)
            machine[rep] = f


    if ex[0] == "andi":
        regs=ex[1].split(",")
        imd=regs[2]
        #print(regs)
        if regData.get(regs[0])!= None and regData.get(regs[1])!= None and regs[0] == regs[1] and -(2**6) < int(imd) < 2**6 :
            #if regs[0] == regs[1] :
            a = inst.get("andi")
            index = int(imd)
            if index < 0:
                imd = ('{:0b}'.format(int(index) & 0xffffffff))[-6:]
            else:
                imd = ('{:0b}'.format(int(index) & 0xffffffff))
                imd = "0" * (6 - len(imd)) + imd
            #print(imd)
            imd=imd[::-1]
            index = regABI.index(regs[0])
            det = (str(bin(index)))[2:]
            det = "0" * (5 - len(det)) + det
            det=det[-3::]
            final=a[0]+imd[5]+a[1]+det+imd[4]+imd[3]+imd[2]+imd[1]+imd[0]+a[3]
            b=hex(int(final,2))
            f=b[2:]
            f = "0" * (4 - len(f)) + f
            rep = assembly.index(i)
            machine[rep] = f

    if ex[0] == "beq":
        regs = ex[1].split(",")
        # imd = regs[1]
        if regData.get(regs[0]) != None and regs[1] == "zero":

            m = machine[assembly.index(i)]
            m = bin(int(m, 16))
            # print(len(m[2:]),m[2:])
            m = (m[2:])
            m = "0" * (31 - len(m)) + m
            m = m[::-1]
            # print(m)
            # print(m[0:31+1])
            imm = m[8:12] + m[25:31] + m[7] + m[31]
            # imm = m[1:5] + m[5:11] + m[11] + m[12]
            # print(imm,len(imm))
            # m = ((bitstring.BitArray("0b"+imm)).bin)
            imm = bitstring.Bits(bin=imm[::-1])
            # print(imm.bin)
            # print(bin(imm))
            # print(imm.int)
            index = imm.int

            # label = raw.index((regs[2])+":")
            # index = label - raw.index(i)
            """if index < 0:
                index += 1
            else:
                index -= 1"""
            # print(label,index)
            index *= 2
            print(index)
            if -256 <= index <= 254:
                a = inst.get("beqz")
                if index < 0:
                    imd = ('{:0b}'.format(index & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(index & 0xffffffff))
                    imd = "0" * (11 - len(imd)) + imd
                # print(imd)
                imd = imd[::-1]
                print(imd[::-1])
                final = a[0] + imd[8] + imd[4] + imd[3] + regData.get(regs[0]) + imd[7] + imd[6] + imd[2] + imd[1] + \
                        imd[
                            5] + a[3]
                # print(final)
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = assembly.index(i)
                machine[rep] = f

    if ex[0] == "beqz":
        regs = ex[1].split(",")
        # imd = regs[1]
        if regData.get(regs[0]) != None:
            m = machine[assembly.index(i)]
            m = bin(int(m, 16))
            m = (m[2:])
            m = "0" * (32 - len(m)) + m
            m = m[::-1]
            imm = m[8:12] + m[25:31] + m[7] + m[31]
            imm = bitstring.Bits(bin=imm[::-1])
            index = imm.int
            index *= 2
            if -256 <= index <= 254:
                a = inst.get("beqz")
                if index < 0:
                    imd = ('{:0b}'.format(int(index) & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(int(index) & 0xffffffff))
                    imd = "0" * (11 - len(imd)) + imd
                # print(index,imd)
                imd = imd[::-1]
                final = a[0] + imd[8] + imd[4] + imd[3] + regData.get(regs[0]) + imd[7] + imd[6] + imd[2] + imd[1] + \
                        imd[
                            5] + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = assembly.index(i)
                machine[rep] = f

    if ex[0] == "bne":
        regs = ex[1].split(",")
        # imd = regs[1]
        if regData.get(regs[0]) != None and regs[1] == "zero":
            # label = raw.index((regs[2]) + ":")
            # index = label - raw.index(i)
            m = machine[assembly.index(i)]
            m = bin(int(m, 16))
            # print(len(m[2:]),m[2:])
            m = (m[2:])
            m = "0" * (32 - len(m)) + m
            m = m[::-1]
            # print(m)
            # print(m[0:31+1])
            imm = m[8:12] + m[25:31] + m[7] + m[31]
            # imm = m[1:5] + m[5:11] + m[11] + m[12]
            # print(imm,len(imm))
            # m = ((bitstring.BitArray("0b"+imm)).bin)
            imm = bitstring.Bits(bin=imm[::-1])
            # print(imm.bin)
            # print(bin(imm))
            # print(imm.int)
            index = imm.int
            # print(index,"aaaaaaaaaaaa")

            """if index < 0:
                index += 1
            else:
                index -= 1"""
            index *= 2
            # print(index,index/2)
            if -256 <= index <= 254:
                a = inst.get("bnez")
                if index < 0:
                    imd = ('{:0b}'.format(int(index) & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(int(index) & 0xffffffff))
                    imd = "0" * (11 - len(imd)) + imd
                imd = imd[::-1]
                final = a[0] + imd[8] + imd[4] + imd[3] + regData.get(regs[0]) + imd[7] + imd[6] + imd[2] + imd[1] + \
                        imd[
                            5] + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = assembly.index(i)
                machine[rep] = f

    if ex[0] == "bnez":
        regs = ex[1].split(",")
        # imd = regs[1]
        if regData.get(regs[0]) != None:
            m = machine[assembly.index(i)]
            m = bin(int(m, 16))
            m = (m[2:])
            m = "0" * (32 - len(m)) + m
            m = m[::-1]
            imm = m[8:12] + m[25:31] + m[7] + m[31]
            imm = bitstring.Bits(bin=imm[::-1])
            index = imm.int
            index *= 2
            if -256 <= index <= 254:
                a = inst.get("bnez")
                if index < 0:
                    imd = ('{:0b}'.format(int(index) & 0xffffffff))[-11:]
                else:
                    imd = ('{:0b}'.format(int(index) & 0xffffffff))
                    imd = "0" * (11 - len(imd)) + imd
                imd = imd[::-1]
                final = a[0] + imd[8] + imd[4] + imd[3] + regData.get(regs[0]) + imd[7] + imd[6] + imd[2] + imd[1] + \
                        imd[
                            5] + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = assembly.index(i)
                machine[rep] = f

    if ex[0]=="jr":
        regs=ex[1].split(",")
        if regs[0] != "zero":
            index = regABI.index(regs[0])
            det = (str(bin(index)))[2:]
            det = "0" * (5 - len(det)) + det
            a=inst.get("jr")
            final=a[0]+det+"00000"+a[3]
            b=hex(int(final,2))
            f=b[2:]
            f = "0" * (4 - len(f)) + f
            rep = assembly.index(i)
            machine[rep] = f

    if ex[0] =="jalr":
        regs=ex[1].split(",")
        #print(regs)
        #print(len(regs))
        if len(regs) == 1:
            if regs[0] != "zero":
                index = regABI.index(regs[0])
                det = (str(bin(index)))[2:]
                det = "0" * (5 - len(det)) + det
                a = inst.get("jalr")
                final = a[0] + det + "00000" + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = assembly.index(i)
                machine[rep] = f
        elif len(regs) == 3:
            #print(regs)
            if regs[0] == "ra" and regs[1] != "zero" and regs[2] == "0":
                print("done")
                index = regABI.index(regs[1])
                det = (str(bin(index)))[2:]
                det = "0" * (5 - len(det)) + det
                a = inst.get("jalr")
                final = a[0] + det + "00000" + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = assembly.index(i)
                machine[rep] = f
            elif regs[0] == "zero" and regs[1] != "zero" and regs[2] == "0":
                index = regABI.index(regs[1])
                det = (str(bin(index)))[2:]
                det = "0" * (5 - len(det)) + det
                a = inst.get("jr")
                final = a[0] + det + "00000" + a[3]
                b = hex(int(final, 2))
                f = b[2:]
                f = "0" * (4 - len(f)) + f
                rep = assembly.index(i)
                machine[rep] = f


#-------------------------------------------------------------------------------------------------------------
#print("--------------------", machine[1])
#------------------------------------------Patching-Code-to-Main-Machine---------------------------------
for index,code in enumerate(machine):
    if len(code) <= 4:
        machineCode[index] = code

#-----------------------------------------Defining Illegal and NOP instructions------------------------------
for index,code in enumerate(machineCode):
    if len(code) <= 4:
        #---------------------------------------------hex to bin--------------
        b = bin(int(code, 32))[2:].zfill(16)
        #---------------------------------------------Illegal instruction-----------
        if b == bin(0)[2:].zfill(16):
            instruction[index] = "\t" + "c.illegal"
        #----------------------------------------------NOP instruction-------------
        elif b == bin(1)[2:].zfill(16):
            instruction[index] = "\t" + "c.nop"

#print(instruction)
ff = open("machine.txt", "w")
for i in machineCode:
    wr =  i + "\n"
    ff.write(wr)
ff.close()

#--------------------------------------------------------------------------------------------------------------KAAAAM KHATAM--------------------------------------------------------------
print("CODE COMPRESSED SUCCESSFULLY")
