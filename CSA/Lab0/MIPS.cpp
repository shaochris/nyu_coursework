#include<iostream>
#include<string>
#include<vector>
#include<bitset>
#include<fstream>
using namespace std;
#define ADDU 1
#define SUBU 3
#define AND 4
#define OR  5
#define NOR 7
#define MemSize 65536 // memory size, in reality, the memory size should be 2^32, but for this lab, for the space resaon, we keep it as this large number, but the memory is still 32-bit addressable.


// TODO:
class RF
{
    public:
        bitset<32> ReadData1, ReadData2; 
     	RF()
    	{ 
          Registers.resize(32);  
          Registers[0] = bitset<32> (0);  
        }
	
        void ReadWrite(bitset<5> RdReg1, bitset<5> RdReg2, bitset<5> WrtReg, bitset<32> WrtData, bitset<1> WrtEnable)
        {   
            // implement the funciton by you. 
            // if(!WrtEnable) {
            //   cout << "Unable to write register" << endl;
            //   exit(1);
            // }
            
            Register[RdReg1.to_ulong()] = WrtData;s
         }
		 
	void OutputRF() // write RF results to file
             {
               ofstream rfout;
                  rfout.open("RFresult.txt",std::ios_base::app);
                  if (rfout.is_open())
                  {
                    rfout<<"A state of RF:"<<endl;
                  for (int j = 0; j<32; j++)
                      {        
                        rfout << Registers[j]<<endl;
                      }
                     
                  }
                  else cout<<"Unable to open file" << endl;
                  rfout.close();
               
               }     
	private:
            vector<bitset<32> >Registers;
	
};

// Done
class ALU
{
      public:
             bitset<32> ALUresult;
             bitset<32> ALUOperation (bitset<3> ALUOP, bitset<32> oprand1, bitset<32> oprand2)
             {   
                 // implement the ALU operations by you.
                 unsigned int result;
                 // if ALUOP is on 
                 if(ALUOP) {
                    result = oprand1.to_ulong() + oprand2.to_ulong();
                 }else {
                    result = oprand1.to_ulong() - oprand2.to_ulong();
                 }
                 return ALUresult = bitset<32>(result);
               }            
};

// Done
class INSMem
{
      public:
          bitset<32> Instruction;
          INSMem() // read instruction memory
          {       IMem.resize(MemSize); 
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
                  else cout<<"Unable to open file imem.txt" << endl;
                  imem.close();
                     
                  }
                  
          bitset<32> ReadMemory (bitset<32> ReadAddress) 
              {    
               // implement by you. (Read the byte at the ReadAddress and the following three byte).
                string sb = "";
                for(int i = 0; i < 4; i++) {
                  sb += IMem[ReadAddress.to_ulong()+i].to_string();
                }
                Instruction = bitset<32>(sb);
                return Instruction;     
              }     
      private:
           vector<bitset<8> > IMem;
      
};

// DONE 
class DataMem    
{
      public:
          bitset<32> readdata;  
          DataMem() // read data memory
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
                  else cout<<"Unable to open file dmem.txt" << endl;
                  dmem.close();
          
          }  
          bitset<32> MemoryAccess (bitset<32> Address, bitset<32> WriteData, bitset<1> readmem, bitset<1> writemem) 
          {    
               if(!(readmem == 1 && writemem ==1)) {
                cout << "Unable to access memory" << endl;
                exit(1);
               }
               string sb;
               for(int i = 0; i < 4; i++) {
                sb.append(DMem[Address.to_ulong()+i].to_string);
               }

               // implement by you.
               return readdata = bitset<32>(sb);     
          }   
                     
          void OutputDataMem()  // write dmem results to file
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
                  else cout<<"Unable to open file dmemresult.txt";
                  dmemout.close();
               
               }             
      
      private:
           vector<bitset<8> > DMem;
      
};

// public variables
bool isRtype;
bool isItype;
bool isJtype;

// components of an instruction
bitset<6> opcode;
bitset<5> rs; // first register
bitset<5> rt; // second register
bitset<5> rd; // target register


// structs for each stage
struct fetch {
  bitset<32> pc;
  bool valid;
};

struct decode {
  bitset<32> instruction;
  bool valid;
};
   
struct execution {
  bitset<32> data1;
  bitset<32> data2;
  bool aluOp;
  bool valid;
};

struct memory {

  bool valid;
};

struct writeback {

  bool valid;
};


// signed extender
bitset<32> signExtend(bitset<16> imm) {
  string result;
  if(imm[15] == 0) {
    result = "0000000000000000" + imm.toString<char,std::string::traits_type,std::string::allocator_type>();
  }else {
    result = "1111111111111111" + imm.toString<char,std::string::traits_type,std::string::allocator_type>();
  }
  return (bitset<32>)result;
}

// struct for stages
struct stage {
  fetch IF;
  decode ID;
  execution EX;
  memory MEM;
  writeback WB;
};

//TODO:
int main()
{
    RF myRF;
    ALU myALU;
    INSMem myInsMem;
    DataMem myDataMem;

    stage status;
    stage newStatus;
    // initialize stage validations
    stage.IF.valid = 0;
    stage.IF.pc = 0;

    stage.ID.valid = 1;

    stage.EX.valid = 1;

    stage.MEM.valid = 1;

    stage.WB.valid = 1;

    
    newStatus = status;
    int cycle = 0;
    while (1)
	  {
      // Fetch
      if(stage.fetch.valid) {
        newStatus.ID.valid = 1;
      }else {
        newStatus.ID.valid = 0;
        // If current insturciton is "11111111111111111111111111111111", then break;
        if(myInsMem.readInstr(stage.IF.pc) == 0xffffffff) {
          newStatus.IF.pc = stage.IF.pc;
          newStatus.IF.valid = 1;
          newStatus.ID.valid = 1;
          newStatus.ID.Instr = 0xffffffff;
        }else {
          newStatus.ID.Instr = myInsMem.readInstr(stage.IF.pc);
          newStatus.IF.pc = bitset<32>(stage.IF.pc.to_ulong()+4);
        }
      }
          
  		// decode(Read RF)
  		
  		// Execute
  		
  		// Read/Write Mem
  		
  		// Write back to RF
		
      myRF.OutputRF(); // dump RF;    
    }
    myDataMem.OutputDataMem(); // dump data mem
  
    return 0;
        
}
