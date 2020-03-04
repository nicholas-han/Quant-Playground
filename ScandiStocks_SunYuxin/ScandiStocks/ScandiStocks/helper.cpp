#include "helper.h"


Date::Date(string date_str, const char delim) {
    if (delim != '\0') {
        if (date_str.length() != 10) throw InvalidDate();
        istringstream iss(date_str);
        string year_str, month_str, day_str;
        getline(iss, year_str, '-');
        getline(iss, month_str, '-');
        getline(iss, day_str, '-');
        year = stoi(year_str);
        month = stoi(month_str);
        day = stoi(day_str);
    }
    else {
        if (date_str.length() != 8) throw InvalidDate();
        year = stoi(date_str.substr(0, 4));
        month = stoi(date_str.substr(4, 2));
        day = stoi(date_str.substr(6, 2));
    }
    if (year < 1000 || year > 10000) throw InvalidDate();
    if (month < 0 || month > 12) throw InvalidDate();
    if (day < 0 || day > 31) throw InvalidDate();
    if (month == 2) {
        if ((year % 4 == 0 && year % 100 != 0) || year % 400 == 0) // leap year
        {
            if (day > 29) throw InvalidDate();
        }
        else {
            if (day > 28) throw InvalidDate();
        }
    }
    else if (month == 4 || month == 6 || month == 9 || month == 11) {
        if (day < 0 || day > 30) throw InvalidDate();
    }
}


ostream& operator<<(ostream& out, const Date& date) {
    out << date.year << "-";
    if (date.month < 10) out << "0";
    out << date.month << "-";
    if (date.day < 10) out << "0";
    out << date.day << endl;
    return out;
}


Tick::Tick(string line) {
    istringstream iss(line);
    string input;
    for (int i = 1; i < ARG_NUM; ++i) {
        getline(iss, input, ',');
        (this->*loaders[i])(input);
    }
}

void Tick::load_stock_symbol(string input) {
    stock_symbol = input;
}

void Tick::load_bid_price(string input) {
    try {
        bid_price = stod(input);
    }
    catch (exception &e) {
        bid_price = 0.0;
    }
}

void Tick::load_ask_price(string input) {
    try {
        ask_price = stod(input);
    }
    catch (exception &e) {
        ask_price = 0.0;
    }
}

void Tick::load_trade_price(string input) {
    try {
        trade_price = stod(input);
    }
    catch (exception &e) {
        trade_price = 0.0;
    }
}

void Tick::load_bid_volume(string input) {
    try {
        bid_volume = stoi(input);
    }
    catch (exception &e) {
        bid_volume = 0;
    }
}

void Tick::load_ask_volume(string input) {
    try {
        ask_volume = stoi(input);
    }
    catch (exception &e) {
        ask_volume = 0;
    }
}

void Tick::load_trade_volume(string input) {
    try {
        trade_volume = stoi(input);
    }
    catch (exception &e) {
        trade_volume = 0;
    }
}

void Tick::load_update_type(string input) {
    try {
        update_type = stoi(input);
    }
    catch (exception &e) {
        update_type = 0;
    }
}

void Tick::load_date(string input) {
    try {
        date = Date(input, '\0');
    }
    catch (exception &e) {
        date = Date("19700101", '\0');
    }
}

void Tick::load_time_in_sec(string input) {
    try {
        time_in_sec = stold(input);
    }
    catch (exception &e) {
        time_in_sec = 0;
    }
}

void Tick::load_open_price(string input) {
    try {
        open_price = stod(input);
    }
    catch (exception &e) {
        open_price = 0.0;
    }
}

void Tick::load_condition_code(string input) {
    condition_code = input;
}


ostream& operator<<(ostream& out, const Tick& tick) {
    out << "Tick: " << tick.stock_symbol << "\t";
    out << setprecision(2) << fixed << tick.bid_price << "\t";
    out << tick.ask_price << "\t";
    out << tick.trade_price << "\t";
    out << tick.bid_volume << "\t";
    out << tick.ask_volume << "\t";
    out << tick.trade_volume << "\t";
    out << tick.update_type << "\t";
    out << tick.date << "\t";
    out << setprecision(6) << fixed << tick.time_in_sec << "\t";
    out << setprecision(2) << fixed << tick.open_price << "\t";
    out << tick.condition_code << endl;
    return out;
}


vector<Tick> loadDataByRow(const string fileName, const int DEBUG_CT=0) {
    vector<Tick> rows;
    ifstream infile;
    infile.open(fileName);
    if(!infile.is_open()) throw std::runtime_error("Could not open file");

    string line;
    getline(infile, line); // igniore column headers
    if (DEBUG_CT) {
        int debug_ct = 0;
        while(getline(infile, line)) {
            if (debug_ct >= DEBUG_CT) break;
            rows.push_back(Tick(line));
            ++debug_ct;
        }
    }
    else {
        while(getline(infile, line))
            rows.push_back(Tick(line));
    }

    infile.close();
    return rows;
}
