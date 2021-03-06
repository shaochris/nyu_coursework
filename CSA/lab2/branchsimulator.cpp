// Lab2
#include <iostream>
#include <fstream>
#include <math.h>
#include <vector>
#include <unordered_map>
#include <deque>
#include <sstream>
#include <bitset>
using namespace std;

int main (int argc, char** argv) {
	ifstream config;
	config.open(argv[1]);

	int m, k;
	config >> m >> k;
 
	config.close();

	ofstream out;
	string out_file_name = string(argv[2]) + ".out";
	out.open(out_file_name.c_str());
	
	ifstream trace;
	trace.open(argv[2]);

	// create saturating counter and BHR
	int num_SC = pow(2,m);
	int num_BHR = pow(2,k);
	vector<vector<bitset<2>	 > > SC(num_BHR+1,vector<bitset<2> >(num_SC+1));

	int BHR_record = 0;
	unordered_map<string, int> BHR;

	for(int i = 0; i < num_BHR; i++) {

		for(int j = 0; j < num_SC; j++) {
			SC[i][j] = bitset<2>(3);
		}
	}

	deque<string> global_history;
	for(int i = 0; i < k; i++) {
		global_history.push_back("1");
	}
	while (!trace.eof()) {
		unsigned long pc; int taken;
		trace >> std::hex >> pc >> taken;
		int prediction = 1;

		bitset<32> pc_b = bitset<32>(pc);

		int PTH_index = stoi((pc_b.to_string()).substr(32-m, 32), nullptr, 2);

		string temp = "";
		for(auto v : global_history) {
			temp.append(v);
		}
		int BHR_index = 0;

		if(BHR.find(temp) == BHR.end()) {
			BHR[temp] = BHR_record;
			BHR_index = BHR[temp];
			BHR_record++;
			
		} else {
			BHR_index = BHR[temp];

		}

		string pre_prediction = (SC[BHR_index][PTH_index]).to_string();
		prediction = stoi(pre_prediction.substr(0,1), nullptr, 2);

		stringstream ss;
		ss << taken;
		string new_history;
		ss >> new_history;

		global_history.pop_back();
		global_history.push_front(new_history);

		out << prediction;

		if(prediction == 1 && taken == 1) {
			if((SC[BHR_index][PTH_index]).to_ulong() != 3)
				SC[BHR_index][PTH_index] = bitset<2>((SC[BHR_index][PTH_index]).to_ulong() + 1);

		} else if (prediction == 0 && taken == 0) {
			if((SC[BHR_index][PTH_index]).to_ulong() != 0)
				SC[BHR_index][PTH_index] = bitset<2>((SC[BHR_index][PTH_index]).to_ulong() - 1);

		} else if (prediction == 1 && taken == 0) {
			if((SC[BHR_index][PTH_index]).to_ulong() == 2)
				SC[BHR_index][PTH_index] = bitset<2>((SC[BHR_index][PTH_index]).to_ulong() - 2);
			else if((SC[BHR_index][PTH_index]).to_ulong() == 3)
				SC[BHR_index][PTH_index] = bitset<2>((SC[BHR_index][PTH_index]).to_ulong() - 1);

		} else if (prediction == 0 && taken == 1) {
			if((SC[BHR_index][PTH_index]).to_ulong() == 1)
				SC[BHR_index][PTH_index] = bitset<2>((SC[BHR_index][PTH_index]).to_ulong() + 2);
			else if((SC[BHR_index][PTH_index]).to_ulong() == 0)
				SC[BHR_index][PTH_index] = bitset<2>((SC[BHR_index][PTH_index]).to_ulong() + 1);
		}

	}

	trace.close();	
	out.close();
}
