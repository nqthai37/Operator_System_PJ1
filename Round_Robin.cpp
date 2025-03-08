#include "Round_Robin.h"

// void readInputFile(string filename);
// // take type, process, quatum if type is RR

// void RoundRobin();
// // RR algorithm to schedule the process
// // return two result, WT, TAR
// void printResult();
// // print to the output file
vector<string> split(string str, string token) {
  vector<string> result;
  while (str.size()) {
    int index = str.find(token);
    if (index != string::npos) {
      result.push_back(str.substr(0, index));
      str = str.substr(index + token.size());
      if (str.size() == 0) result.push_back(str);
    } else {
      result.push_back(str);
      str = "";
    }
  }
  return result;
}

void Schedule::readInputFile(string filename) {
  ifstream file(filename);
  if (!file.is_open()) {
    cout << "File not found" << endl;
    return;
  }
  file >> type;
  if (type == 2) {
    file >> quantum;
  }
  file >> number_of_process;
  string line = "";
  for (int i = 0; i < number_of_process; i++) {
    vector<string> temp;
    getline(file, line);
    temp = split(line, " ");
    process.push_back(temp);
  }
}