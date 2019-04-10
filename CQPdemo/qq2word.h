#pragma once
#include <string>
using namespace std;

string qq2word(int64_t qq) {
    string temp = to_string(qq);
    for (int i = 0; i < temp.length(); i++) temp[i] = temp[i] * 2 + 1;
    return temp;
}