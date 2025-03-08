#include <iostream>
#include <fstream>
#include <string>
#include <vector>
using namespace std;

class Schedule {
 private:
  int type;
  int number_of_process;
  vector<vector<string>> process;
  int quantum;
  vector<string> result_CPU;
  vector<int> result_R;
  int WaitingTime;
  int TurnAroundTime;

  void readInputFile(string filename);
  // take type, process, quatum if type is RR

  void RoundRobin();
  // RR algorithm to schedule the process
  // return two result, WT, TAR
  void printResult();
  // print to the output file
};