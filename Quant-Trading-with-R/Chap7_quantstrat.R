################ Installation ################
install.packages("devtools") # if not installed
install.packages("FinancialInstrument") #if not installed
install.packages("PerformanceAnalytics") #if not installed

# next install blotter from GitHub
devtools::install_github("braverock/blotter")
# next install quantstrat from GitHub
devtools::install_github("braverock/quantstrat")

##############################################

library(quantstrat)
# Supress warnings
options("getSymbols.warning4.0"=FALSE)
# Do some house cleaning
rm(list=ls(.blotter), envir=.blotter)
# Set currency and timezone
currency('USD')
Sys.setenv(TZ="UTC")
# Define symbols of interest
symbols <- c("XLE", # SPDR Energy sector
             "XLF", # SPDR Financial sector
             "XLI", # SPDR Industrial sector
             "XLU", # SPDR Utility sector
             "XLK", # SPDR Tech sector
             "RWR", # Dow Jones REIT ETF
             "EWJ", # iShares Japan
             "EWG", # iShares Germany
             "EWU", # iShares UK
             "EWY", # iShares Korea
             "EPP" # iShares Pacific Ex Japan
             )

suppressMessages(getSymbols(symbols, from="2016-01-01", to="2018-11-01", src="yahoo", adjust=TRUE))









