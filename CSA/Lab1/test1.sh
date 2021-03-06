#!/usr/bin/env zsh



if [ -f 'dmem.txt' -a -f 'imem.txt' -a -f 'Instructions.txt' ]; then
	rm dmem.txt imem.txt Instructions.txt
fi

cp ./Testbenches/testbench_hazards_no_stall/dmem.txt .
cp ./Testbenches/testbench_hazards_no_stall/imem.txt .
cp ./Testbenches/testbench_hazards_no_stall/Instructions.txt .
if [ -f 'dmemresult.txt' ]; then
	rm dmemresult.txt
fi
if [ -f 'RFresult.txt' ]; then
	rm RFresult.txt
fi
if [ -f 'stateresult.txt' ]; then
	rm stateresult.txt
fi

if [ -f 'MIPS_pipeline' ]; then
	make clean
fi

make 

./MIPS_pipeline


# no stalls
echo "priting dmem comparison"
diff dmemresult.txt ./Testbenches/testbench_hazards_no_stall/dmemresult.txt

echo "priting RF comparison"
diff RFresult.txt ./Testbenches/testbench_hazards_no_stall/RFresult.txt

echo "priting state comparison"
diff stateresult.txt ./Testbenches/testbench_hazards_no_stall/stateresult.txt

# rm dmemresult.txt RFresult.txt stateresult.txt