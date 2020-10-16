#On my honor, I have neither given nor received unauthorized aid on this assignment
import sys
def C1(content,instr_index,start):
    category1={
        "0000":J,"0001":JR,"0010":BEQ,"0011":BLTZ,"0100":BGTZ,"0101":BREAK,"0110":SW,"0111":LW,"1000":SLL,"1001":SRL,"1010":SRA,"1011":NOP
        }
    method=category1.get(content)
    if method:
        result = method(instr_index,start)
        return result

def C2(content,instr_index,start):
    category2={
        "0000":ADD,"0001":SUB,"0010":MUL,"0011":AND,"0100":OR,"0101":XOR,"0110":NOR,"0111":SLT,"1000":ADDI,"1001":ANDI,"1010":ORI,"1011":XORI
        }
    method=category2.get(content)
    if method:
        result = method(instr_index,start)
        return result

def start_execute(zhiling):
    execute={
        "J":J_simulate,"JR":JR_simulate,"BEQ":BEQ_simulate,"BLTZ":BLTZ_simulate,"BGTZ":BGTZ_simulate,"BREAK":BREAK_simulate,"SW":SW_simulate,"LW":LW_simulate,"SLL":SLL_simulate,"SRL":SRL_simulate,
        "SRA":SRA_simulate,"NOP":NOP_simulate,"ADD":ADD_simulate,"SUB":SUB_simulate,"MUL":MUL_simulate,"AND":AND_simulate,"OR":OR_simulate,"XOR":XOR_simulate,
        "NOR":NOR_simulate,"SLT":SLT_simulate,"ADDI":ADDI_simulate,"ANDI":ANDI_simulate,"ORI":ORI_simulate,"XORI":XORI_simulate
    }
    method=execute.get(zhiling[0])
    if method:
        result = method(zhiling)
        return result

def J(instr_index,start):
    jump=int(instr_index,2)*4
    ins_content[start]=["J",jump]
    return "J "+"#"+str(jump)

def J_simulate(zhiling):
    global index
    index=zhiling[1]

def JR(instr_index,start):
    rs=int(instr_index[:5],2)
    ins_content[start]=["JR",rs]
    return "JR R" +str(rs)

def JR_simulate(zhiling):
    global index
    index=register[zhiling[1]]

def BEQ(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    offset=flip_plus(instr_index[10:])*4
    ins_content[start]=["BEQ",rs,rt,offset]
    return "BEQ R"+str(rs)+", R"+str(rt)+", #" + str(offset)

def BEQ_simulate(zhiling):
    global index
    if register[zhiling[1]]==register[zhiling[2]]:
        index+=(zhiling[3]+4)
    else:
        index+=4

def BLTZ(instr_index,start):
    rs=int(instr_index[:5],2)
    offset=flip_plus(instr_index[15:])*4
    ins_content[start]=["BLTZ",rs,offset]
    return "BLTZ R"+str(rs)+", #" + str(offset)

def BLTZ_simulate(zhiling):
    global index
    if zhiling[1]<0:
        index+=(zhiling[2]+4)
    else:
        index+=4
        
def BGTZ(instr_index,start):
    rs=int(instr_index[:5],2)
    offset=flip_plus(instr_index[10:])*4
    ins_content[start]=["BGTZ",rs,offset]
    return "BGTZ R"+str(rs)+", #" + str(offset)

def BGTZ_simulate(zhiling):
    global index
    if register[zhiling[1]]>0:
        index+=(zhiling[2]+4)
    else:
        index+=4

def BREAK(instr_index,start):
    global stop
    stop=True
    ins_content[start]=["BREAK"]
    return "BREAK"

def BREAK_simulate(zhiling):
    global tingzhi
    tingzhi=True

def SW(instr_index,start):
    base=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    offset=flip_plus(instr_index[10:])
    ins_content[start]=["SW",rt,offset,base]
    return "SW R"+ str(rt) +", "+str(offset)+"(" +"R" + str(base)+ ")"

def SW_simulate(zhiling):
    global index
    index+=4
    start_ins[zhiling[2]+register[zhiling[3]]]=register[zhiling[1]]

def LW(instr_index,start):
    base=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    offset=flip_plus(instr_index[10:])
    ins_content[start]=["LW",rt,offset,base]
    return "LW R"+ str(rt) +", "+str(offset)+"(" +"R" + str(base)+ ")"

def LW_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=start_ins[zhiling[2]+register[zhiling[3]]]

def SLL(instr_index,start):
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    sa=int(instr_index[15:20],2)
    ins_content[start]=["SLL",rd,rt,sa]
    return "SLL R"+str(rd)+", R"+str(rt) + ", #" + str(sa)

def SLL_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=register[zhiling[2]]*(2**zhiling[3])

def SRL(instr_index,start):
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    sa=int(instr_index[15:20],2)
    ins_content[start]=["SRL",rd,rt,sa]
    return "SRL R"+str(rd)+", R"+str(rt) + ", #" + str(sa)

def SRL_simulate(zhiling):
    global index
    index+=4
    if register[zhiling[2]]>0:
         register[zhiling[1]]//=register[zhiling[2]]*zhiling[3]
    else:
        temp=bin(register[zhiling[2]] & 0b11111111111111111111111111111111)[2:]
        num="0"*zhiling[3]+str(temp[:(-1)*zhiling[3]])
        register[zhiling[1]]=(int(num,2))

def SRA(instr_index,start):
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    sa=int(instr_index[15:20],2)
    ins_content[start]=["SRA",rd,rt,sa]
    return "SRA R"+str(rd)+", R"+str(rt) + ", #" + str(sa)

def SRA_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=register[zhiling[2]]>>zhiling[3]

def NOP(instr_index,start):
    ins_content[start]=["NOP"]
    return "NOP"

def NOP_simulate(zhiling):
    global index
    index+=4

def ADD(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["ADD",rd,rs,rt]
    return "ADD R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def ADD_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=register[zhiling[2]]+register[zhiling[3]]

def SUB(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["SUB",rd,rs,rt]
    return "SUB R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def SUB_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=register[zhiling[2]]-register[zhiling[3]]

def MUL(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["MUL",rd,rs,rt]
    return "MUL R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def MUL_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=register[zhiling[2]]*register[zhiling[3]]

def AND(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["AND",rd,rs,rt]
    return "AND R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def AND_simulate(zhiling):
    temp=register[zhiling[2]]
    temp&=register[zhiling[3]]
    register[zhiling[1]]=temp
    global index
    index+=4

def OR(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["OR",rd,rs,rt]
    return "OR R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def OR_simulate(zhiling):
    register[zhiling[1]]=(register[zhiling[3]]|register[zhiling[2]])
    global index
    index+=4

def XOR(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["XOR",rd,rs,rt]
    return "XOR R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def XOR_simulate(zhiling):
    register[zhiling[1]]=(register[zhiling[2]]^register[zhiling[3]])
    global index
    index+=4

def NOR(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["NOR",rd,rs,rt]
    return "NOR R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def NOR_simulate(zhiling):
    a=register[zhiling[2]]
    b=register[zhiling[3]]
    register[zhiling[1]]=~(a|b)

    global index
    index+=4

def SLT(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    rd=int(instr_index[10:15],2)
    ins_content[start]=["SLT",rd,rs,rt]
    return "SLT R"+str(rd)+", R"+str(rs)+", R" + str(rt)

def SLT_simulate(zhiling):
    global index
    index+=4
    if register[zhiling[2]]<register[zhiling[3]]:
        register[zhiling[1]]=1
    else:
        register[zhiling[1]]=0

def ADDI(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    immediate=flip_plus(instr_index[10:])
    ins_content[start]=["ADDI",rt,rs,immediate]
    return "ADDI R"+str(rt)+", R"+str(rs)+", #" + str(immediate)

def ADDI_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=register[zhiling[2]]+zhiling[3]

def ANDI(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    immediate=int(instr_index[10:],2)
    ins_content[start]=["ANDI",rt,rs,immediate]
    return "ANDI R"+str(rt)+", R"+str(rs)+", #" + str(immediate)

def ANDI_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=(register[zhiling[2]]&zhiling[3])

def ORI(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    immediate=int(instr_index[10:],2)
    ins_content[start]=["ORI",rt,rs,immediate]
    return "ORI R"+str(rt)+", R"+str(rs)+", #" + str(immediate)

def ORI_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=(register[zhiling[2]]|zhiling[3])

def XORI(instr_index,start):
    rs=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    immediate=int(instr_index[10:],2)
    ins_content[start]=["XORI",rt,rs,immediate]
    return "XORI R"+str(rt)+", R"+str(rs)+", #" + str(immediate)

def XORI_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=(register[zhiling[2]]^zhiling[3])

def flip(instruction):
    ib_string = ""
    for bit in instruction:
        if bit == "1":
            ib_string += "0"
        elif bit == "0":
            ib_string += "1"
    return ib_string

def flip_plus(instruction):
    if instruction[0]=="1":
        ib_string = ""
        for bit in instruction:
            if bit == "1":
                ib_string += "0"
            elif bit == "0":
                ib_string += "1"
        return (int(ib_string,2)+1)*(-1)
    else:
        return int(instruction,2)

if __name__ == "__main__":
    filename=sys.argv[1]
    f1=open(filename,"r")
    f2=open("disassembly.txt","w")
    f3=f1.readlines()
    f4=open("simulation.txt","w")
    stop=False#代表遇没遇到break指令
    start=256#写死的从256开始
    ins_content={}#存的是指令+包含的数字
    start_ins={}#存的是256对应的指令/data
    start1,start2=0,0
    for instruction in f3:
        category=instruction[0:2]
        content=instruction[2:6]
        instr_index=instruction[6:]
        if not stop:
            if category == "01":
                ins=C1(content,instr_index,start)
                start_ins[start]=ins
                result = instruction.strip('\n') +"\t" + str(start) + "\t"+ins
                f2.write(result)
                f2.write('\n')
            if category == "11":
                ins=C2(content,instr_index,start)
                start_ins[start]=ins
                result = instruction.strip('\n') +"\t" + str(start) + "\t"+ins
                f2.write(result)
                f2.write('\n')
            start+=4
            start1=start
        else:
            judge=instruction[0]
            if judge=="0":
                start_ins[start]=int(instruction,2)
                result= instruction.strip('\n') + "\t" + str(start) + "\t"+str(int(instruction,2))
                f2.write(result)
                f2.write('\n')
            else:
                start_ins[start]=(int(flip(instruction),2)+1)*(-1)
                result= instruction.strip('\n') + "\t" + str(start) + "\t"+ "-"+str(int(flip(instruction),2)+1)
                f2.write(result)
                f2.write('\n')
            start+=4
    start2=start-4
    register=[0 for i in range(32) ]
    cycle,index=1,256
    tingzhi=False
    cnt=0
    while (not tingzhi):
        f4.write("--------------------"+"\n")
        f4.write("Cycle "+str(cycle)+":"+"\t"+str(index)+"\t"+str(start_ins[index])+"\n")
        start_execute(ins_content[index])
        f4.write("\n"+"Registers"+"\n")
        f4.write("R00:" +"\t"+ str(register[0])+"\t"+str(register[1])+"\t"+str(register[2])+"\t"+str(register[3])+"\t"+str(register[4])+"\t"+str(register[5])+"\t"+str(register[6])+"\t"+str(register[7])+"\n")
        f4.write("R08:" +"\t"+ str(register[8])+"\t"+str(register[9])+"\t"+str(register[10])+"\t"+str(register[11])+"\t"+str(register[12])+"\t"+str(register[13])+"\t"+str(register[14])+"\t"+str(register[15])+"\n")
        f4.write("R16:" +"\t"+ str(register[16])+"\t"+str(register[17])+"\t"+str(register[18])+"\t"+str(register[19])+"\t"+str(register[20])+"\t"+str(register[21])+"\t"+str(register[22])+"\t"+str(register[23])+"\n")
        f4.write("R24:" +"\t"+ str(register[24])+"\t"+str(register[25])+"\t"+str(register[26])+"\t"+str(register[27])+"\t"+str(register[28])+"\t"+str(register[29])+"\t"+str(register[30])+"\t"+str(register[31])+"\n")
        cycle+=1
        f4.write("\n")
        f4.write("Data")
        i=start1
        while i < start2+4:
            if (i-start1)%32==0:
                f4.write("\n")
                f4.write(str(i)+":"+"\t")
            f4.write(str(start_ins[i])+"\t")
            i+=4
        f4.write("\n")
        f4.write("\n")



