@echo off

rem Define the CSV files
set "nifty=D:\trading\weekly_options\data\output_nifty.csv"
set "banknifty=D:\trading\weekly_options\data\output_banknifty.csv"

rem Clean up CSV nifty
echo Cleaning up %nifty%...
type nul > %nifty%
echo Cleanup of %nifty% complete.

rem Clean up CSV banknifty
echo Cleaning up %banknifty%...
type nul > %banknifty%
echo Cleanup of %banknifty% complete.

echo Data cleanup process completed for both CSV files.
