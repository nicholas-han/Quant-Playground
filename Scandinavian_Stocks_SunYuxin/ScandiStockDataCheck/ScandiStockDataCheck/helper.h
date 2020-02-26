#ifndef HELPER_H
#define HELPER_H

#include <fstream>
#include <sstream>

#include <vector>

using namespace std;


struct InvalidDate : public exception {
   const char * what () const throw () {
      return "Exception: Invalid Date";
   }
};


class Date {
public:
    Date() {};
    Date(string date_str, const char delim);
    friend ostream& operator<<(ostream& out, const Date& date);

private:
    int year, month, day;
};


class Tick {
public:
    Tick(string line); // constructor
    
    // loaders
    void load_stock_symbol(string input);
    void load_bid_price(string input);
    void load_ask_price(string input);
    void load_trade_price(string input);
    void load_bid_volume(string input);
    void load_ask_volume(string input);
    void load_trade_volume(string input);
    void load_update_type(string input);
    void load_date(string input);
    void load_time_in_sec(string input);
    void load_open_price(string input);
    void load_condition_code(string input);
    inline void dummy_load(string input) {}
    
    // operator overloading
    friend ostream& operator<<(ostream& out, const Tick& tick);

private:
    // fields
    const uint8_t ARG_NUM = 16;
    string stock_symbol, condition_code;
    double bid_price, ask_price, trade_price, open_price;
    int bid_volume, ask_volume, trade_volume, update_type;
    long double time_in_sec;
    Date date;

    // function pointer
    void (Tick::*loaders[16])(string) = {
        [0] = &Tick::dummy_load,
        [1] = &Tick::load_stock_symbol,
        [2] = &Tick::dummy_load,
        [3] = &Tick::load_bid_price,
        [4] = &Tick::load_ask_price,
        [5] = &Tick::load_trade_price,
        [6] = &Tick::load_bid_volume,
        [7] = &Tick::load_ask_volume,
        [8] = &Tick::load_trade_volume,
        [9] = &Tick::load_update_type,
        [10] = &Tick::dummy_load,
        [11] = &Tick::load_date,
        [12] = &Tick::load_time_in_sec,
        [13] = &Tick::load_open_price,
        [14] = &Tick::dummy_load,
        [15] = &Tick::load_condition_code,
    };
    
};


vector<Tick> loadDataByRow(const string fileName, const int DEBUG_CT);

#endif /* HELPER_H */
