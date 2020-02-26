#include <iostream>

#include <string>
#include <vector>

#include "helper.h"

using namespace std;


int main(int argc, const char *argv[]) {
    // load data
    string abs_file_path = "/Users/nhan/git/Quant-Playground/Scandinavian_Stocks_SunYuxin/ScandiStockDataCheck/ScandiStockDataCheck/scandi.csv";
    vector<Tick> rows = loadDataByRow(abs_file_path, 5);
    // print data
    for (size_t i = 0, n = rows.size(); i < n; ++i)
        cout << rows[i] << endl;
    // TODO: remove bad/irrelevant ticks
    // TODO: calculate statistics

    return 0;
}
