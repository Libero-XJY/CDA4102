#On my honor, I have neither given nor received unauthorized aid on this assignment
from operator import pos
from os import remove
import sys
def C1(content,instr_index,PC):
    category1={
        "0000":J,"0001":JR,"0010":BEQ,"0011":BLTZ,"0100":BGTZ,"0101":BREAK,"0110":SW,"0111":LW,"1000":SLL,"1001":SRL,"1010":SRA,"1011":NOP
        }
    method=category1.get(content)
    if method:
        result = method(instr_index,PC)
        return result

def C2(content,instr_index,PC):
    category2={
        "0000":ADD,"0001":SUB,"0010":MUL,"0011":AND,"0100":OR,"0101":XOR,"0110":NOR,"0111":SLT,"1000":ADDI,"1001":ANDI,"1010":ORI,"1011":XORI
        }
    method=category2.get(content)
    if method:
        result = method(instr_index,PC)
        return result

def PC_execute(zhiling):
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

def J_pipeline(zhiling):
    global index
    index=zhiling[1]

def JR(instr_index,start):
    rs=int(instr_index[:5],2)
    ins_content[start]=["JR",rs]
    return "JR R" +str(rs)

def JR_simulate(zhiling):
    global index
    index=register[zhiling[1]]

def JR_pipeline(zhiling):
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

def BEQ_pipeline(zhiling):
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

def BLTZ_pipeline(zhiling):
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

def BGTZ_pipeline(zhiling):
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

def BREAK_pipeline(zhiling):
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
    PC_ins[zhiling[2]+register[zhiling[3]]]=register[zhiling[1]]

def SW_pipeline(zhiling):
    PC_ins[zhiling[2]+register[zhiling[3]]]=register[zhiling[1]]

def LW(instr_index,start):
    base=int(instr_index[:5],2)
    rt=int(instr_index[5:10],2)
    offset=flip_plus(instr_index[10:])
    ins_content[start]=["LW",rt,offset,base]
    return "LW R"+ str(rt) +", "+str(offset)+"(" +"R" + str(base)+ ")"

def LW_simulate(zhiling):
    global index
    index+=4
    register[zhiling[1]]=PC_ins[zhiling[2]+register[zhiling[3]]]

def LW_pipeline(zhiling):
    register[zhiling[1]]=PC_ins[zhiling[2]+register[zhiling[3]]]

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

def SLL_pipeline(zhiling):
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

def SRL_pipeline(zhiling):
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

def SRA_pipeline(zhiling):
    register[zhiling[1]]=register[zhiling[2]]>>zhiling[3]

def NOP(instr_index,start):
    ins_content[start]=["NOP"]
    return "NOP"

def NOP_simulate(zhiling):
    global index
    index+=4

def NOP_pipeline(zhiling):
    pass

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
    
def ADD_pipeline(zhiling):
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

def SUB_pipeline(zhiling):
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

def MUL_pipeline(zhiling):
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

def AND_pipeline(zhiling):
    temp=register[zhiling[2]]
    temp&=register[zhiling[3]]
    register[zhiling[1]]=temp

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

def OR_pipeline(zhiling):
    register[zhiling[1]]=(register[zhiling[3]]|register[zhiling[2]])

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

def XOR_pipeline(zhiling):
    register[zhiling[1]]=(register[zhiling[2]]^register[zhiling[3]])

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

def NOR_pipeline(zhiling):
    a=register[zhiling[2]]
    b=register[zhiling[3]]
    register[zhiling[1]]=~(a|b)

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

def SLT_pipeline(zhiling):
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

def ADDI_pipeline(zhiling):
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

def ANDI_pipeline(zhiling):
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

def ORI_pipeline(zhiling):
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

def XORI_pipeline(zhiling):
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

def fetch():
    global Temp_ins
    global index
    global jump
    jump=False
    if index+4<=max_index:
            fetch_queue.append(index)
            fetch_queue.append(index+4)
    elif index<=max_index:
            fetch_queue.append(index)
    if len(fetch_queue)==2 and len(pre_issue)==3:
            fetch_queue.pop()
    if waiting_instruction or executed_instruction:
        if executed_instruction:
            temp_pc=executed_instruction.pop()
            instruction=ins_content[temp_pc]
            Temp_ins=PC_ins[temp_pc]
            if instruction[0]=="JR":
                JR_pipeline(instruction)
            elif instruction[0]=="BLTZ":
                BLTZ_pipeline(instruction)
            elif instruction[0]=="BEQ":
                BEQ_pipeline(instruction)
            elif instruction[0]=="BGTZ":
                BGTZ_pipeline(instruction)
            jump=True#这个circle发生过跳转        
        if waiting_instruction:
            instruction=ins_content[waiting_instruction[0]]
            if not ready_fetch(instruction):
                temp_pc=waiting_instruction.pop()
                Temp_ins=PC_ins[temp_pc]
                executed_instruction.append(temp_pc)
                if instruction[0]=="JR":
                    JR_pipeline(instruction)
                elif instruction[0]=="BLTZ":
                    BLTZ_pipeline(instruction)
                elif instruction[0]=="BEQ":
                    BEQ_pipeline(instruction)
                elif instruction[0]=="BGTZ":
                    BGTZ_pipeline(instruction)
                jump=True#这个circle发生过跳转  
                executed_instruction.clear()    
        fetch_queue.clear()#无空位就clear 
        return #然后return，就当无事发生
    if len(pre_issue)==4:
        fetch_queue.clear()
    if fetch_queue:
        buffer_fetch_queue=fetch_queue[:]
        for i in buffer_fetch_queue:
            instruction=ins_content[i]
            if instruction[0] in branch:#如果是JR BEQ BLTZ BGTZ
                if len(buffer_fetch_queue)==2 and buffer_fetch_queue.index(i)==1:
                    branch_reg=[]
                    if instruction[0]=="JR":
                        branch_reg.append(instruction[1])
                    elif instruction[0]=="BLTZ":
                        branch_reg.append(instruction[1])
                    elif instruction[0]=="BEQ":
                        branch_reg.append(instruction[1])
                        branch_reg.append(instruction[2])
                    elif instruction[0]=="BGTZ":
                        branch_reg.append(instruction[1])
                    prev_register=get_fetch_register([buffer_fetch_queue[0]])
                    if set(prev_register)&set(branch_reg):
                        waiting_instruction.append(i)
                        fetch_queue.remove(i)
                        continue
                if not ready_fetch(instruction):#查看他们有没有ready_fetch
                    executed_instruction.append(i)
                    fetch_queue.remove(i)
                    Temp_ins=PC_ins[i]
                    if instruction[0]=="JR":
                        JR_pipeline(instruction)
                    elif instruction[0]=="BLTZ":
                        BLTZ_pipeline(instruction)
                    elif instruction[0]=="BEQ":
                        BEQ_pipeline(instruction)
                    elif instruction[0]=="BGTZ":
                        BGTZ_pipeline(instruction)
                    jump=True#这个circle发生过跳转
                    executed_instruction.clear() 
                else:
                    waiting_instruction.append(i)
                    fetch_queue.remove(i)
                break#后面的都不要了
            elif instruction[0] in other_branch:#如果是BREAK J NOP
                executed_instruction.append(i)#如果是J BREAK直接丢到executed里去
                fetch_queue.remove(i)
                Temp_ins=PC_ins[i]
                jump=True
                if instruction[0]=="J":
                    Temp_ins=PC_ins[i]
                    J_pipeline(instruction)
                    jump=True
                    executed_instruction.clear()
                elif instruction[0]=="BREAK":
                    BREAK_pipeline(instruction)
                break
            elif instruction[0]=="NOP":
                NOP_simulate(instruction)
            else:
                if fetch_queue and len(pre_issue)+len(fetch_buffer)<4:
                    fetch_buffer.append(i)
                    fetch_queue.remove(i) 
    fetch_queue.clear()#fetch结束后fetch queue也就没用了，issue部分要用到的东西都放在了fetch_buffer里。

def issue():
    global cnt
    already_one_mem=False
    already_one_alu2=False
    if not pre_issue:#队列为空，啥也不干
        return
    issue_buffer=[]#最多只能存两个
    for i in pre_issue:
        instruction=ins_content[i]
        if ready_issue(instruction) or eariler_not_issued(pre_issue.index(i)):#rule 2 and rule 4 and rule 5，我觉得5包含在2/4里面了
            continue
        if instruction[0] in ["SW","LW"]:#rule 6 and rule 7
            if store_before(pre_issue.index(i)) or already_one_mem:
                continue
        if instruction[0] in ["ADD","SUB","MUL","AND","OR","XOR","NOR","SLT","ADDI","ANDI","XORI","ORI","SLL","SRL","SRA"]:
            if already_one_alu2:
                continue
        if len(issue_buffer)<2:#把index加入到buffer里面
            if instruction[0] in ["SW","LW"]:
                already_one_mem=True
            if instruction[0] in ["ADD","SUB","MUL","AND","OR","XOR","NOR","SLT","ADDI","ANDI","XORI","ORI","SLL","SRL","SRA"]:
                already_one_alu2=True
            issue_buffer.append(pre_issue.index(i))
        # print("issue buffer",issue_buffer)
    if len(issue_buffer)==2:#rule 3
        if check_harzard_between_two(issue_buffer):
            issue_buffer.pop()
    #rule1
    ins1=ins2=None
    have_two=False
    if len(issue_buffer)==2:
        have_two=True
        ins1=pre_issue[issue_buffer[0]]
        ins2=pre_issue[issue_buffer[1]]
    elif len(issue_buffer)==1:
        ins1=pre_issue[issue_buffer[0]]
    instrcution1=instrcution2=None
    if issue_buffer:
        instrcution1=ins_content[ins1]
        if instrcution1[0] in ["SW","LW"]:
            pre_alu1.append(ins1)
            pre_issue.remove(ins1)
        else:
            pre_alu2.append(ins1)
            pre_issue.remove(ins1)
        if have_two:
            instrcution2=ins_content[ins2]
            if instrcution2[0] in ["SW","LW"]:
                pre_alu1.append(ins2)
                pre_issue.remove(ins2)
            else:
                pre_alu2.append(ins2)
                pre_issue.remove(ins2)
    issue_buffer.clear()

def fetch2():#把fecth_buffer的pc丢到pre issue queue
    global index
    global jump
    if not fetch_buffer:
        return
    while fetch_buffer and len(pre_issue)<4:
        if not jump:#这个circle没发生过跳转
            index+=4
        pre_issue.append(fetch_buffer.pop(0))
    fetch_buffer.clear()

def wb():
    if post_mem:
        wb_1.append(post_mem.pop(0))
    if post_alu2:
        wb_2.append(post_alu2.pop(0))
    post_alu2.clear()
    post_mem.clear()

def post():
    if pre_mem:
        pc=pre_mem.pop(0)
        instruction=ins_content[pc]
        if instruction[0]=="SW":
            SW_pipeline(instruction)
        else:
            post_mem.append(pc)
    pre_mem.clear()

def mem():
    if pre_alu2:
        post_alu2.append(pre_alu2.pop(0))
    if pre_alu1:
        pre_mem.append(pre_alu1.pop(0))

def get_issue_register(all_data_structure):
    occupied=[]
    for i in all_data_structure:#i is pc
        if ins_content[i][0] in["ADD","SUB","MUL","AND","OR","XOR","NOR","SLT"]:
             occupied.append(ins_content[i][1])
             occupied.append(ins_content[i][2])
             occupied.append(ins_content[i][3])
        elif ins_content[i][0] in ["ADDI","ANDI","XORI","ORI","SLL","SRL","SRA"]:
            occupied.append(ins_content[i][1])
            occupied.append(ins_content[i][2])
        elif ins_content[i][0]=="LW" or ins_content[i][0]=="SW":
            occupied.append(ins_content[i][1])
            occupied.append(ins_content[i][3])
    return occupied
    
def get_fetch_register(all_data_structure):#获取后面数据结构所有在写的寄存器，大家都是1。
    occupied=[]
    for i in all_data_structure:#i is pc
        if ins_content[i][0] in["ADD","SUB","MUL","AND","OR","XOR","NOR","SLT","ADDI","ANDI","XORI","ORI","LW","SLL","SRL","SRA"]:
             occupied.append(ins_content[i][1])
    return occupied

def ready_issue(instruction):#查看当前扫描到的pre issued的指令和后面的数据结构有没有冲突
    reg_ins_occupied=[]#当前指令涉及到的寄存器
    if instruction[0] in["ADD","SUB","MUL","AND","OR","XOR","NOR","SLT"]:
        reg_ins_occupied.append(instruction[1])
        reg_ins_occupied.append(instruction[2])
        reg_ins_occupied.append(instruction[3])
    elif instruction[0] in ["ADDI","ANDI","XORI","ORI","SLL","SRL","SRA"]:
        reg_ins_occupied.append(instruction[1])
        reg_ins_occupied.append(instruction[2])
    elif instruction[0]=="LW" or instruction[0]=="SW":
        reg_ins_occupied.append(instruction[1])
        reg_ins_occupied.append(instruction[3])
    all_data_structure=pre_mem+post_mem+post_alu2+wb_1+wb_2+pre_alu1+pre_alu2#issue后面的数据结构的汇总
    ds_ins_occupied=get_fetch_register(all_data_structure)
    if list(set(reg_ins_occupied)&set(ds_ins_occupied)):#有交集就不行
        return True
    else :
        return False

def check_harzard_between_two(issue_buffer):
    first,second=issue_buffer[0],issue_buffer[1]
    first_read,first_write=reg_pre_issue(ins_content[pre_issue[first]])
    second_read,second_write=reg_pre_issue(ins_content[pre_issue[second]])
    if list(set(first_write)&set(second_write)) or list(set(first_write)&set(second_read)) or list(set(first_read)&set(second_write)):
        return True
    else:
        return False

def reg_pre_issue(instruction):#查看当前扫描到的pre issued的指令涉及到的寄存器
    read,write=[],[]
    if instruction[0] in["ADD","SUB","MUL","AND","OR","XOR","NOR","SLT"]:
        write.append(instruction[1])
        read.append(instruction[2])
        read.append(instruction[3])
    elif instruction[0] in ["ADDI","ANDI","XORI","ORI","SLL","SRL","SRA"]:
        write.append(instruction[1])
        read.append(instruction[2])
    elif instruction[0]=="LW":
        write.append(instruction[1])
        read.append(instruction[3])
    elif instruction[0]=="SW":
        read.append(instruction[1])
        read.append(instruction[3])
    return read,write

def eariler_not_issued(index):#查看当前指令和他前面的指令有没有冲突
    if index==0:#你是第一所以你可以
        return False
    curr=ins_content[pre_issue[index]]
    curr_read,curr_write=reg_pre_issue(curr)
    for element in pre_issue[:index]:
        prev_read,prev_write=reg_pre_issue(ins_content[element])
        if list(set(curr_write)&set(prev_write)) or list(set(curr_write)&set(prev_read)) or list(set(curr_read)&set(prev_write)):
            return True
    return False

def store_before(index):
    if index==0:#你是第一所以你可以
        return False
    for element in pre_issue[:index]:
        if ins_content[element][0]=="SW":
            return True
    return False

def ready_fetch(instruction):#看看能不能fetch
    reg_ins_occupied=[]
    if instruction[0]=="BEQ":
       reg_ins_occupied[:]=instruction[1:3]
    else:
       reg_ins_occupied.append(instruction[1])
    all_data_structure=pre_issue+pre_mem+post_mem+post_alu2+wb_1+wb_2+pre_alu1+pre_alu2#全部后面的数据结构的汇总
    ds_ins_occupied=get_fetch_register(all_data_structure)
    if list(set(reg_ins_occupied)&set(ds_ins_occupied)):
        return True
    else :
        return False

def execute():
    if wb_1:
        instruction=ins_content[wb_1.pop()]
        if instruction[0]=="LW":
            LW_pipeline(instruction)
    if wb_2:
        instruction=ins_content[wb_2.pop()]
        if instruction[0]=="SLL":
            SLL_pipeline(instruction)
        elif instruction[0]=="SRL":
            SRL_pipeline(instruction)
        elif instruction[0]=="SRA":
            SRA_pipeline(instruction)
        elif instruction[0]=="ADD":
            ADD_pipeline(instruction)
        elif instruction[0]=="SUB":
            SUB_pipeline(instruction)
        elif instruction[0]=="MUL":
            MUL_pipeline(instruction)
        elif instruction[0]=="AND":
            AND_pipeline(instruction)
        elif instruction[0]=="OR":
            OR_pipeline(instruction)
        elif instruction[0]=="XOR":
            XOR_pipeline(instruction)
        elif instruction[0]=="NOR":
            NOR_pipeline(instruction)
        elif instruction[0]=="SLT":
            SLT_pipeline(instruction)
        elif instruction[0]=="ADDI":
            ADDI_pipeline(instruction)
        elif instruction[0]=="ANDI":
            ANDI_pipeline(instruction)
        elif instruction[0]=="ORI":
            ORI_pipeline(instruction)
        elif instruction[0]=="XORI":
            XORI_pipeline(instruction)

if __name__ == "__main__":
    filename=sys.argv[1]
    f1=open(filename,"r")
    f2=open("disassembly.txt","w")
    f3=f1.readlines()
    f4=open("simulation.txt","w")
    stop=False#代表遇没遇到break指令
    PC=256#写死的从256开始
    ins_content={}#{256: ['ADD', 1, 0, 0]}
    PC_ins={}#{256: 'ADD R1, R0, R0'}
    PC1,PC2=0,0
    branch=["JR","BEQ","BLTZ","BGTZ"]
    other_branch=["BREAK","J"]
    for instruction in f3:
        category=instruction[0:2]
        content=instruction[2:6]
        instr_index=instruction[6:]
        if not stop:
            if category == "01":
                ins=C1(content,instr_index,PC)
                PC_ins[PC]=ins
                result = instruction.strip('\n') +"\t" + str(PC) + "\t"+ins
                f2.write(result)
                f2.write('\n')
            if category == "11":
                ins=C2(content,instr_index,PC)
                PC_ins[PC]=ins
                result = instruction.strip('\n') +"\t" + str(PC) + "\t"+ins
                f2.write(result)
                f2.write('\n')
            PC+=4
            PC1=PC
        else:
            judge=instruction[0]
            if judge=="0":
                PC_ins[PC]=int(instruction,2)
                result= instruction.strip('\n') + "\t" + str(PC) + "\t"+str(int(instruction,2))
                f2.write(result)
                f2.write('\n')
            else:
                PC_ins[PC]=(int(flip(instruction),2)+1)*(-1)
                result= instruction.strip('\n') + "\t" + str(PC) + "\t"+ "-"+str(int(flip(instruction),2)+1)
                f2.write(result)
                f2.write('\n')
            PC+=4
    max_index=max(ins_content.keys())
    PC2=PC-4
    jump=False
    register=[0 for i in range(32) ]
    #f4.write(PC_ins)#only use when f4.write the result
    #f4.write(register)#这是寄存器，[value,是否被占用]
    #f4.write(ins_content)#256: ['ADD', 1, 0, 0]  pc和对应的指令，非数字版本。
    circle,index=1,256
    fetch_buffer=[]#用来存已经拿好的指令，在issue部分的真issue结束后丢到pre issue queue里去。
    fetch_queue,pre_issue,pre_alu1,pre_alu2,waiting_instruction,executed_instruction,pre_mem,post_mem,post_alu2,wb_1,wb_2=[],[],[],[],[],[],[],[],[],[],[]
    tingzhi=False
    jump=None
    Temp_ins=None
    cnt=1
    while not tingzhi:
        f4.write("--------------------"+"\n")
        f4.write("Cycle "+ str(cnt)+":"+"\n")
        f4.write("\n")
        f4.write("IF Unit: "+"\n")
        wb()
        post()
        mem()
        fetch()
        if len(fetch_buffer)==2 and len(pre_issue)==3:
            fetch_buffer.pop()
        issue()
        fetch2()
        execute()
        if not waiting_instruction:
            f4.write("\t"+"Waiting Instruction: "+"\n")
        else:
            f4.write("\t"+"Waiting Instruction: "+"["+str(PC_ins[waiting_instruction[0]])+"]"+"\n")
        if jump:
            f4.write("\t"+"Executed Instruction: " + "["+str(Temp_ins)+"]"+"\n")
        else:
            f4.write("\t"+"Executed Instruction:"+"\n")
        if not pre_issue:
            f4.write("Pre-Issue Queue: "+"\n")
            f4.write("\t"+"Entry 0:"+"\n")
            f4.write("\t"+"Entry 1:"+"\n")
            f4.write("\t"+"Entry 2:"+"\n")
            f4.write("\t"+"Entry 3:"+"\n")
        elif len(pre_issue)==1:
            f4.write("Pre-Issue Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_issue[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:"+"\n")
            f4.write("\t"+"Entry 2:"+"\n")
            f4.write("\t"+"Entry 3:"+"\n")
        elif len(pre_issue)==2:
            f4.write("Pre-Issue Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_issue[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:" "["+str(PC_ins[pre_issue[1]])+"]"+"\n")
            f4.write("\t"+"Entry 2:"+"\n")
            f4.write("\t"+"Entry 3:"+"\n")
        elif len(pre_issue)==3:
            f4.write("Pre-Issue Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_issue[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:" "["+str(PC_ins[pre_issue[1]])+"]"+"\n")
            f4.write("\t"+"Entry 2:" "["+str(PC_ins[pre_issue[2]])+"]"+"\n")
            f4.write("\t"+"Entry 3:"+"\n")
        elif len(pre_issue)==4:
            f4.write("Pre-Issue Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_issue[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:" "["+str(PC_ins[pre_issue[1]])+"]"+"\n")
            f4.write("\t"+"Entry 2:" "["+str(PC_ins[pre_issue[2]])+"]"+"\n")
            f4.write("\t"+"Entry 3:" "["+str(PC_ins[pre_issue[3]])+"]"+"\n")
        if not pre_alu1:
            f4.write("Pre-ALU1 Queue: "+"\n")
            f4.write("\t"+"Entry 0:"+"\n")
            f4.write("\t"+"Entry 1:"+"\n")
        elif len(pre_alu1)==1:
            f4.write("Pre-ALU1 Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_alu1[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:"+"\n")
        elif len(pre_alu1)==2:
            f4.write("Pre-ALU1 Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_alu1[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:" "["+str(PC_ins[pre_alu1[1]])+"]"+"\n")
        if pre_mem:
            f4.write("Pre-MEM Queue: "+ "["+str(PC_ins[pre_mem[0]])+"]"+"\n")
        else:
            f4.write("Pre-MEM Queue: "+"\n")
        if post_mem:
            f4.write("Post-MEM Queue: "+ "["+str(PC_ins[post_mem[0]])+"]"+"\n")
        else:
            f4.write("Post-MEM Queue: "+"\n")
        if not pre_alu2:
            f4.write("Pre-ALU2 Queue: "+"\n")
            f4.write("\t"+"Entry 0:"+"\n")
            f4.write("\t"+"Entry 1:"+"\n")
        elif len(pre_alu2)==1:
            f4.write("Pre-ALU2 Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_alu2[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:"+"\n")
        elif len(pre_alu2)==2:
            f4.write("Pre-ALU2 Queue: "+"\n")
            f4.write("\t"+"Entry 0:" "["+str(PC_ins[pre_alu2[0]])+"]"+"\n")
            f4.write("\t"+"Entry 1:" "["+str(PC_ins[pre_alu2[1]])+"]"+"\n")
        if post_alu2:
            f4.write("Post-ALU2 Queue: " + "["+str(PC_ins[post_alu2[0]])+"]"+"\n")
        else:
            f4.write("Post-ALU2 Queue: "+"\n")
        f4.write("\n")
        f4.write("Registers"+"\n")
        f4.write("R00:" +"\t"+ str(register[0])+"\t"+str(register[1])+"\t"+str(register[2])+"\t"+str(register[3])+"\t"+str(register[4])+"\t"+str(register[5])+"\t"+str(register[6])+"\t"+str(register[7])+"\n")
        f4.write("R08:" +"\t"+ str(register[8])+"\t"+str(register[9])+"\t"+str(register[10])+"\t"+str(register[11])+"\t"+str(register[12])+"\t"+str(register[13])+"\t"+str(register[14])+"\t"+str(register[15])+"\n")
        f4.write("R16:" +"\t"+ str(register[16])+"\t"+str(register[17])+"\t"+str(register[18])+"\t"+str(register[19])+"\t"+str(register[20])+"\t"+str(register[21])+"\t"+str(register[22])+"\t"+str(register[23])+"\n")
        f4.write("R24:" +"\t"+ str(register[24])+"\t"+str(register[25])+"\t"+str(register[26])+"\t"+str(register[27])+"\t"+str(register[28])+"\t"+str(register[29])+"\t"+str(register[30])+"\t"+str(register[31])+"\n")
        f4.write("\n")
        f4.write("Data")
        cnt+=1 
        i=PC1
        while i < PC2+4:
            if (i-PC1)%32==0:
                f4.write("\n")
                f4.write(str(i)+":"+"\t")
            f4.write(str(PC_ins[i])+"\t")
            i+=4
        f4.write("\n")