# data_processing.py

import json
import csv


class DataProcessor:
    def __init__(self, json_file_path, num_strikes=4, strike_increment=50, lot_size=50):
        self.json_file_path = json_file_path
        self.num_strikes = num_strikes
        self.strike_increment = strike_increment
        self.lot_size = lot_size
        self.collected_data = []
        self.total_ce_open_interest = 0
        self.total_pe_open_interest = 0
        self.diff = 0
        self.pcr = None
        self.option_signal = "neutral"
        self.timestamp = None
        self.underlying_value = None

    def process_json_data(self):
        with open(self.json_file_path, "r") as file:
            json_data = json.load(file)

        self.timestamp = json_data["records"]["timestamp"]
        self.underlying_value = json_data["records"]["underlyingValue"]
        lower_strike = self.underlying_value - (
            self.num_strikes * self.strike_increment
        )
        upper_strike = self.underlying_value + (
            (self.num_strikes + 1) * self.strike_increment
        )

        data = json_data["filtered"]["data"]

        for item in data:
            expiry_date = item.get("expiryDate", "")
            ce_open_interest = item.get("CE", {}).get("openInterest", None)
            pe_open_interest = item.get("PE", {}).get("openInterest", None)
            strike_price = item.get("strikePrice", None)

            if lower_strike <= strike_price <= upper_strike:
                self.collected_data.append(
                    (expiry_date, strike_price, ce_open_interest, pe_open_interest)
                )
                self.total_ce_open_interest += (
                    ce_open_interest if ce_open_interest is not None else 0
                )
                self.total_pe_open_interest += (
                    pe_open_interest if pe_open_interest is not None else 0
                )

            self.diff = abs(
                self.total_pe_open_interest * self.lot_size
                - self.total_ce_open_interest * self.lot_size
            )

    def calculate_pcr(self):
        if self.total_ce_open_interest != 0:
            self.pcr = round(
                self.total_pe_open_interest / self.total_ce_open_interest, 3
            )
        else:
            self.pcr = 0

    def determine_option_signal(self):
        if self.pcr is not None:
            if self.pcr > 1.25:
                self.option_signal = "buy ce"
            elif self.pcr < 0.75:
                self.option_signal = "buy pe"

    def write_to_csv(self, csv_file_path):
        with open(csv_file_path, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    self.timestamp,
                    self.underlying_value,
                    self.diff,
                    self.pcr,
                    self.option_signal,
                ]
            )
