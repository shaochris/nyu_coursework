#include<iostream>
#include<string>
#include<vector>
#include<bitset>
#include<fstream>
using namespace std;
#define MemSize 1000 // memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.

struct IFStruct {
    bitset<32>  PC;
    bool        nop;  
};

struct IDStruct {
    bitset<32>  Instr;
    bool        nop;  
};

struct EXStruct {
    bitset<32>  Read_data1;
    bitset<32>  Read_data2;
    bitset<16>  Imm;
    bitset<5>   Rs;
    bitset<5>   Rt;
    bitset<5>   Wrt_reg_addr;
    bool        is_I_type;
    bool        rd_mem;
    bool        wrt_mem; 
    bool        alu_op;     //1 for addu, lw, sw, 0 for subu 
    bool        wrt_enable;
    bool        nop;  
};

struct MEMStruct {
    bitset<32>  ALUresult;
    bitset<32>  Store_data;
    bitset<5>   Rs;
    bitset<5>   Rt;    
    bitset<5>   Wrt_reg_addr;
    bool        rd_mem;
    bool        wrt_mem; 
    bool        wrt_enable;    
    bool        nop;    
};

struct WBStruct {
    bitset<32>  Wrt_data;
    bitset<5>   Rs;
    bitset<5>   Rt;     
    bitset<5>   Wrt_reg_addr;
    bool        wrt_enable;
    bool        nop;     
};

struct stateStruct {
    IFStruct    IF;
    IDStruct    ID;
    EXStruct    EX;
    MEMStruct   MEM;
    WBStruct    WB;
};

class RF
{
    public: 
        bitset<32> Reg_data;
     	RF()
    	{ 
			Registers.resize(32);  
			Registers[0] = bitset<32> (0);  
        }
	
        bitset<32> readRF(bitset<5> Reg_addr)
        {   
            Reg_data = Registers[Reg_addr.to_ulong()];
            return Reg_data;
        }
    
        void writeRF(bitset<5> Reg_addr, bitset<32> Wrt_reg_data)
        {
            Registers[Reg_addr.to_ulong()] = Wrt_reg_data;
        }
		 
		void outputRF()
		{
			ofstream rfout;
			rfout.open("RFresult.txt",std::ios_base::app);
			if (rfout.is_open())
			{
				rfout<<"State of RF:\t"<<endl;
				for (int j = 0; j<32; j++)
				{        
					rfout << Registers[j]<<endl;
				}
			}
			else cout<<"Unable to open file";
			rfout.close();               
		} 
			
	private:
		vector<bitset<32> >Registers;	
};

// import from MIPS_solution.cpp
class ALU
{
    public:
        bitset<32> ALUresult;
        bitset<32> ALUOperation (bool ALUOP, bitset<32> oprand1, bitset<32> oprand2)
        {
            unsigned int result;

            if(ALUOP) // addu
                result = oprand1.to_ulong() + oprand2.to_ulong();
            else // subu
                result = oprand1.to_ulong() - oprand2.to_ulong();    
            return ALUresult = bitset<32> (result);
        }
};

class INSMem
{
	public:
        bitset<32> Instruction;
        INSMem()
        {       
			IMem.resize(MemSize); 
            ifstream imem;
			string line;
			int i=0;
			imem.open("imem.txt");
			if (imem.is_open())
			{
				while (getline(imem,line))
				{      
					IMem[i] = bitset<8>(line);
					i++;
				}                    
			}
            else cout<<"Unable to open file";
			imem.close();                     
		}
                  
		bitset<32> readInstr(bitset<32> ReadAddress) 
		{    
			string insmem;
			insmem.append(IMem[ReadAddress.to_ulong()].to_string());
			insmem.append(IMem[ReadAddress.to_ulong()+1].to_string());
			insmem.append(IMem[ReadAddress.to_ulong()+2].to_string());
			insmem.append(IMem[ReadAddress.to_ulong()+3].to_string());
			Instruction = bitset<32>(insmem);		//read instruction memory
			return Instruction;     
		}     
      
    private:
        vector<bitset<8> > IMem;     
};
      
class DataMem    
{
    public:
        bitset<32> ReadData;  
        DataMem()
        {
            DMem.resize(MemSize); 
            ifstream dmem;
            string line;
            int i=0;
            dmem.open("dmem.txt");
            if (dmem.is_open())
            {
                while (getline(dmem,line))
                {      
                    DMem[i] = bitset<8>(line);
                    i++;
                }
            }
            else cout<<"Unable to open file";
                dmem.close();          
        }
		
        bitset<32> readDataMem(bitset<32> Address)
        {	
			string datamem;
            datamem.append(DMem[Address.to_ulong()].to_string());
            datamem.append(DMem[Address.to_ulong()+1].to_string());
            datamem.append(DMem[Address.to_ulong()+2].to_string());
            datamem.append(DMem[Address.to_ulong()+3].to_string());
            ReadData = bitset<32>(datamem);		//read data memory
            return ReadData;               
		}
            
        void writeDataMem(bitset<32> Address, bitset<32> WriteData)            
        {
            DMem[Address.to_ulong()] = bitset<8>(WriteData.to_string().substr(0,8));
            DMem[Address.to_ulong()+1] = bitset<8>(WriteData.to_string().substr(8,8));
            DMem[Address.to_ulong()+2] = bitset<8>(WriteData.to_string().substr(16,8));
            DMem[Address.to_ulong()+3] = bitset<8>(WriteData.to_string().substr(24,8));  
        }   
                     
        void outputDataMem()
        {
            ofstream dmemout;
            dmemout.open("dmemresult.txt");
            if (dmemout.is_open())
            {
                for (int j = 0; j< 1000; j++)
                {     
                    dmemout << DMem[j]<<endl;
                }
                     
            }
            else cout<<"Unable to open file";
            dmemout.close();               
        }             
      
    private:
		vector<bitset<8> > DMem;      
};  

void printState(stateStruct state, int cycle)
{
    ofstream printstate;
    printstate.open("stateresult.txt", std::ios_base::app);
    if (printstate.is_open())
    {
        printstate<<"State after executing cycle:\t"<<cycle<<endl; 
        
        printstate<<"IF.PC:\t"<<state.IF.PC.to_ulong()<<endl;        
        printstate<<"IF.nop:\t"<<state.IF.nop<<endl; 
        
        printstate<<"ID.Instr:\t"<<state.ID.Instr<<endl; 
        printstate<<"ID.nop:\t"<<state.ID.nop<<endl;
        
        printstate<<"EX.Read_data1:\t"<<state.EX.Read_data1<<endl;
        printstate<<"EX.Read_data2:\t"<<state.EX.Read_data2<<endl;
        printstate<<"EX.Imm:\t"<<state.EX.Imm<<endl; 
        printstate<<"EX.Rs:\t"<<state.EX.Rs<<endl;
        printstate<<"EX.Rt:\t"<<state.EX.Rt<<endl;
        printstate<<"EX.Wrt_reg_addr:\t"<<state.EX.Wrt_reg_addr<<endl;
        printstate<<"EX.is_I_type:\t"<<state.EX.is_I_type<<endl; 
        printstate<<"EX.rd_mem:\t"<<state.EX.rd_mem<<endl;
        printstate<<"EX.wrt_mem:\t"<<state.EX.wrt_mem<<endl;        
        printstate<<"EX.alu_op:\t"<<state.EX.alu_op<<endl;
        printstate<<"EX.wrt_enable:\t"<<state.EX.wrt_enable<<endl;
        printstate<<"EX.nop:\t"<<state.EX.nop<<endl;        

        printstate<<"MEM.ALUresult:\t"<<state.MEM.ALUresult<<endl;
        printstate<<"MEM.Store_data:\t"<<state.MEM.Store_data<<endl; 
        printstate<<"MEM.Rs:\t"<<state.MEM.Rs<<endl;
        printstate<<"MEM.Rt:\t"<<state.MEM.Rt<<endl;   
        printstate<<"MEM.Wrt_reg_addr:\t"<<state.MEM.Wrt_reg_addr<<endl;              
        printstate<<"MEM.rd_mem:\t"<<state.MEM.rd_mem<<endl;
        printstate<<"MEM.wrt_mem:\t"<<state.MEM.wrt_mem<<endl; 
        printstate<<"MEM.wrt_enable:\t"<<state.MEM.wrt_enable<<endl;         
        printstate<<"MEM.nop:\t"<<state.MEM.nop<<endl;        

        printstate<<"WB.Wrt_data:\t"<<state.WB.Wrt_data<<endl;
        printstate<<"WB.Rs:\t"<<state.WB.Rs<<endl;
        printstate<<"WB.Rt:\t"<<state.WB.Rt<<endl;        
        printstate<<"WB.Wrt_reg_addr:\t"<<state.WB.Wrt_reg_addr<<endl;
        printstate<<"WB.wrt_enable:\t"<<state.WB.wrt_enable<<endl;        
        printstate<<"WB.nop:\t"<<state.WB.nop<<endl; 
    }
    else cout<<"Unable to open file";
    printstate.close();
}

// import fram MIPS_solution.cpp
unsigned long shiftbits(bitset<32> inst, int start)
{
    unsigned long ulonginst;
    return ((inst.to_ulong())>>start);
    
}



bitset<32> signextend (bitset<16> imm)
{
    string sestring;
    if (imm[15]==0){
        sestring = "0000000000000000"+imm.to_string<char,std::string::traits_type,std::string::allocator_type>();    
    }
    else{
        sestring = "1111111111111111"+imm.to_string<char,std::string::traits_type,std::string::allocator_type>();
    }
    return (bitset<32> (sestring));

}

int main()
{
    // instruction segments
    bitset<6> opcode;
    bitset<5> rs;
    bitset<5> rt;
    bitset<5> rd;
    bitset<16> imm;
    // bitset<5> shamt;
    bitset<6> funct;
    bitset<32> extendimm;
    bitset<32> pcAddr;

    // determine instruction
    bool isItype;
    bool isBranch;
    bool isLoad;
    bool isStore;
    bool aluOp;
    bool writeEnable;
    bool stall1;
    bool stall2;

    // structures
    RF myRF;
    INSMem myInsMem;
    DataMem myDataMem;
	ALU myALU;
    // creating state object and initialize wrt_enables and nops
    stateStruct state, newState;

    
    // boolean states and cycle initialziation
    int cycle = 0;
    // all nops should be initialzied to 1 except IF since it is the starting stage of the pipeline.
    // 0 -> off 1 -> on

    // stalls
    stall1 = 0;
    stall2 = 0;

    // IF
    state.IF.PC = 0;
    state.IF.nop = 0;

    // ID
    state.ID.nop = 1;

    // EX
    state.EX.is_I_type = 0;
    state.EX.rd_mem = 0;
    state.EX.wrt_mem = 0;
    state.EX.alu_op = 1;
    state.EX.wrt_enable = 0;
    state.EX.nop = 1;

    // MEM
    state.MEM.rd_mem = 0;
    state.MEM.wrt_mem = 0;
    state.MEM.wrt_enable = 0;
    state.MEM.nop = 1;

    // WB
    state.WB.wrt_enable = 0;
    state.WB.nop = 1;

    // initial for next instruction
    newState = state;

    while (1) {
        /* --------------------- WB stage --------------------- */
        if(!state.WB.nop) {
            if(state.WB.wrt_enable)
                myRF.writeRF(state.WB.Wrt_reg_addr, state.WB.Wrt_data);
            
        }

        /* --------------------- MEM stage --------------------- */
        if(state.MEM.nop)
        {
            newState.WB.nop = 1;
        }
        else
        {
            newState.WB.nop = 0;
            if(state.MEM.rd_mem)
            {
                myDataMem.readDataMem(state.MEM.ALUresult);
                newState.WB.Wrt_data = myDataMem.ReadData;

            }
            else if(state.MEM.wrt_mem)
            {
                bitset<32> storeData = state.MEM.Store_data;
                if(state.WB.Wrt_reg_addr == state.MEM.Rt)
                    storeData = state.WB.Wrt_data;
                myDataMem.writeDataMem(state.MEM.ALUresult, storeData);
            }
            else
            {   
                // beq
                newState.WB.Wrt_data = state.MEM.wrt_enable ? state.MEM.ALUresult : state.WB.Wrt_data;          
            }
            newState.WB.Rs           = state.MEM.Rs;
            newState.WB.Rt           = state.MEM.Rt;
            newState.WB.Wrt_reg_addr = state.MEM.Wrt_reg_addr;
            newState.WB.wrt_enable   = state.MEM.wrt_enable;
        }

        /* --------------------- EX stage --------------------- */

          if(state.EX.nop)
          {
            newState.MEM.nop = 1;
          }
          else
          {
            newState.MEM.nop = 0;
            bitset<32> data1 = state.EX.Read_data1;
            bitset<32> data2 = state.EX.Read_data2;
            if(state.WB.wrt_enable)
            {
                if(state.WB.Wrt_reg_addr == state.EX.Rs)
                    data1 = state.WB.Wrt_data;
                if(state.WB.Wrt_reg_addr == state.EX.Rt)
                    data2 = state.WB.Wrt_data;
            }

            if(state.MEM.wrt_enable)
            {
                if(state.MEM.Wrt_reg_addr == state.EX.Rs)
                    data1 = state.MEM.rd_mem ? myDataMem.ReadData : state.MEM.ALUresult;
                if(state.MEM.Wrt_reg_addr == state.EX.Rt)
                    data2 = state.MEM.rd_mem ? myDataMem.ReadData : state.MEM.ALUresult;
            }


            if(state.EX.is_I_type) //beq
                myALU.ALUOperation(state.EX.alu_op, data1, signextend(state.EX.Imm));
            else // addu, subu
                myALU.ALUOperation(state.EX.alu_op, data1, data2);

            // passing value to mem
            newState.MEM.ALUresult = myALU.ALUresult;
            // beq
            newState.MEM.ALUresult = (!state.EX.is_I_type && !state.EX.wrt_enable) ? 0 : myALU.ALUresult;
            
            data2 = (state.WB.Wrt_reg_addr == state.EX.Rt) ? state.WB.Wrt_data : state.EX.Read_data2;

            newState.MEM.Store_data   = data2;
            newState.MEM.Rs           = state.EX.Rs;
            newState.MEM.Rt           = state.EX.Rt;
            newState.MEM.Wrt_reg_addr = state.EX.Wrt_reg_addr;
            newState.MEM.rd_mem       = state.EX.rd_mem;
            newState.MEM.wrt_mem      = state.EX.wrt_mem;
            newState.MEM.wrt_enable   = state.EX.wrt_enable;
          }

        /* --------------------- ID stage --------------------- */


        if(state.ID.nop)
        {
            newState.EX.nop = 1;
        }
        else
        {  
            newState.EX.nop = 0;
            bitset<32> instruction = state.ID.Instr;
            opcode      = bitset<6> (shiftbits(instruction, 26));
            funct       = bitset<6> (shiftbits(instruction, 0));
            isItype     = (opcode.to_ulong() == 0)    ? 0 : 1;
            // i type instructions
            isBranch    = (opcode.to_ulong() == 0x04) ? 1 : 0;
            isLoad      = (opcode.to_ulong() == 0x23) ? 1 : 0;
            isStore     = (opcode.to_ulong() == 0x2B) ? 1 : 0;
            writeEnable = (isStore || isBranch)       ? 0 : 1;
            // aluOp 1 on addu, lw, sw
            aluOp       = (opcode.to_ulong() == 0x21 || opcode.to_ulong() == 0x2B || opcode.to_ulong() == 0x00) ? 1 : 0;
            // aluOp 0 on subu
            aluOp       = (opcode.to_ulong() == 0x00 && funct.to_ulong() == 0x23) ? 0 : 1;
            rs          = bitset<5> (shiftbits(instruction, 21));
            rt          = bitset<5> (shiftbits(instruction, 16));
            rd          = isItype ? rt : bitset<5> (shiftbits(instruction, 11));
            imm         = bitset<16> (shiftbits(instruction, 0));
            extendimm   = signextend(imm);
            // cout << state.IF.PC.to_ulong() << endl;
            // cout << bitset<30> (shiftbits(extendimm, 0)).to_string() + "00" << endl;
            // cout << extendimm << endl;
            bitset<32> temp = bitset<32> (bitset<30> (shiftbits(extendimm, 0)).to_string() + "00");
            pcAddr          = bitset<32>(state.IF.PC.to_ulong() + temp.to_ulong());

            if(isBranch)
            {
                // if not equal then stall and jump
                // actually bne
                if(myRF.readRF(rs) != myRF.readRF(rt))
                    stall2 = 1;
            }
            else 
            {
                if(!isItype)
                {
                    if((state.EX.Wrt_reg_addr == rt && state.EX.rd_mem))
                        stall1 = 1;
                }
                newState.EX.is_I_type = isItype;
            }

            // passing values to EX stage
            newState.EX.Read_data1   = myRF.readRF(rs);
            newState.EX.Read_data2   = myRF.readRF(rt);
            newState.EX.Imm          = imm;
            newState.EX.Rs           = rs;
            newState.EX.Rt           = rt;
            newState.EX.Wrt_reg_addr = rd;
            newState.EX.rd_mem       = isLoad;
            newState.EX.wrt_mem      = isStore;
            newState.EX.alu_op       = aluOp;
            newState.EX.wrt_enable   = writeEnable;

        }
        

        /* --------------------- IF stage --------------------- */
        if(state.IF.nop)
        {
            newState.ID.nop = 1;
        } 
        else
        {
            newState.ID.nop = 0;
            // if fetching halt, then set nop to 1
            if(myInsMem.readInstr(state.IF.PC) == 0b11111111111111111111111111111111)
            {
                // setting nop of ID and IF to 1 and pass halt instruction to ID
                newState.IF.PC    = state.IF.PC;
                newState.IF.nop   = 1;
                newState.ID.nop   = 1;
                newState.ID.Instr = 0b11111111111111111111111111111111;
            }
            else
            {
                // pass instrtucion to ID and incrase PC by 4
                newState.ID.Instr = myInsMem.readInstr(state.IF.PC);
                newState.IF.PC = bitset<32> (state.IF.PC.to_ulong()+4);

            }
        }

        // if stalls
        if(stall1) 
        {
            stall1          = 0;
            newState.IF     = state.IF;
            newState.ID     = state.ID;
            newState.EX.nop = 1;

        }

        if(stall2)
        {
            stall2          = 0;
            newState.IF.PC  = pcAddr;
            newState.ID     = state.ID;
            newState.IF.nop = 0;
            newState.ID.nop = 1;
        }

        /* --------------------- HALT --------------------- */ 
        if (state.IF.nop && state.ID.nop && state.EX.nop && state.MEM.nop && state.WB.nop)
            break;
        // test
        // if(cycle > 5) break;

        printState(newState, cycle); //print states after executing cycle 0, cycle 1, cycle 2 ... 
        cycle++;
        state = newState; /*The end of the cycle and updates the current state with the values calculated in this cycle */ 
                	

    }
    
    myRF.outputRF(); // dump RF;	
	myDataMem.outputDataMem(); // dump data mem 
	
	return 0;
}
