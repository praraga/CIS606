/*
  Displaying process segment addresses
*/
#include <iostream>
extern int etext, edata, end;
using namespace std;
int
main( ){
  cout << "Adr etext: " << hex << int(&etext) << "\t ";
  cout << "Adr edata: " << hex << int(&edata) << "\t ";
  cout << "Adr end: " << hex << int(&end ) << "\n";
  return 0;
}