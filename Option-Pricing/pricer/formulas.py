import sys
import numpy as np
from datetime import datetime, date, time, timedelta
import pandas as pd
from scipy.stats import norm

class Option:

    def __init__(self, debug=False, **args):

        if not debug: # NOTE: don't show TraceBack if not in debug mode
            sys.tracebacklimit = 0

        self.parity = None
        self.spot = None
        self.strike = None
        self.intRate = None
        self.divYield = None
        self.vol = None
        self.optionPrice = None
        self.timeToMat = None

        self.volDays = 270.0

        self._loadParams(**args)

    def updateParams(self, **args):
        self._loadParams(**args)


    def bsPrice(self, **args):
        self._loadParams(**args)
        self._checkParams(['self.parity', 'self.spot', 'self.strike', 'self.intRate', \
                            'self.divYield', 'self.vol', 'self.timeToMat'])

        parity = self.parity
        spot = self.spot
        strike = self.strike
        intRate = self.intRate
        divYield = self.divYield
        vol = self.vol
        timeToMat = self.timeToMat

        d1 = 1 / (vol * np.sqrt(timeToMat)) * (np.log(spot/strike) + (intRate - divYield + vol**2 / 2) * timeToMat)
        d2 = d1 - vol * np.sqrt(timeToMat)

        if parity == 'call':
            price = norm.cdf(d1) * spot * np.exp(-divYield*timeToMat) - \
                                    norm.cdf(d2) * strike * np.exp(-intRate*timeToMat)
        if parity == 'put':
            price =  norm.cdf(-d2) * strike * np.exp(-intRate*timeToMat) - \
                                    norm.cdf(-d1) * spot * np.exp(-divYield*timeToMat)

        return price


    def bsGreeks(self, **args):

        self._loadParams(**args)
        self._checkParams(['self.parity', 'self.spot', 'self.strike', 'self.intRate', \
                            'self.divYield', 'self.vol', 'self.timeToMat'])
        
        parity = self.parity
        spot = self.spot
        strike = self.strike
        intRate = self.intRate
        divYield = self.divYield
        vol = self.vol
        timeToMat = self.timeToMat

        d1 = 1 / (vol * np.sqrt(timeToMat)) * (np.log(spot/strike) + (intRate - divYield + vol**2 / 2) * timeToMat)
        d2 = d1 - vol * np.sqrt(timeToMat)

        outputDict = {}

        if parity == 'call':
            outputDict['Price'] = norm.cdf(d1) * spot * np.exp(-divYield*timeToMat) - \
                                    norm.cdf(d2) * strike * np.exp(-intRate*timeToMat)
            outputDict['Delta'] = np.exp(-divYield*timeToMat) * norm.cdf(d1)
            outputDict['Theta'] = (-spot * np.exp(-divYield*timeToMat) * norm.pdf(d1) * vol / 2 / np.sqrt(timeToMat) - \
                                    intRate * strike * np.exp(-intRate*timeToMat) * norm.cdf(d2) + \
                                    divYield * spot * np.exp(-divYield*timeToMat) * norm.cdf(d1)) / self.volDays
            outputDict['Rho'] = strike * timeToMat * np.exp(-intRate*timeToMat) * norm.cdf(d2) / 100
        if parity == 'put':
            outputDict['price'] =  norm.cdf(-d2) * strike * np.exp(-intRate*timeToMat) - \
                                    norm.cdf(-d1) * spot * np.exp(-divYield*timeToMat)
            outputDict['Delta'] = -np.exp(-divYield*timeToMat) * norm.cdf(-d1)
            outputDict['Theta'] = (-spot * np.exp(-divYield*timeToMat) * norm.pdf(d1) * vol / 2 / np.sqrt(timeToMat) + \
                                    intRate * strike * np.exp(-intRate*timeToMat) * norm.cdf(-d2) - \
                                    divYield * spot * np.exp(-divYield*timeToMat) * norm.cdf(-d1)) / self.volDays
            outputDict['Rho'] = -strike * timeToMat * np.exp(-intRate*timeToMat) * norm.cdf(-d2) / 100
        outputDict['Gamma'] = np.exp(-divYield*timeToMat) * norm.pdf(d1) / (spot * vol * np.sqrt(timeToMat))
        outputDict['Vega'] = spot * np.exp(-divYield*timeToMat) * norm.pdf(d1) * np.sqrt(timeToMat) / 100

        return outputDict


    def bsImpVol(self, **args):

        self._loadParams(**args)
        self._checkParams(['self.parity', 'self.spot', 'self.strike', 'self.intRate', \
                            'self.divYield', 'self.optionPrice', 'self.timeToMat'])

        # compute implied vol
        impVol = 0.50
        while True:            
            outputDict = self.bsGreeks(vol=impVol)
            correction = float((outputDict['Price'] - self.optionPrice) / outputDict['Vega'] / 100)
            impVol -= correction
            if correction < 0.0001:
                break

        outputDict =  self.bsGreeks(vol=impVol)
        outputDict['ImpVol'] = impVol
        del outputDict['Price']

        return outputDict


    def _loadParams(self, **args):

        # checks if inputs are empty, of wrong type or in invalid range
        ## option parity type
        if 'parity' in args:
            parity = args['parity']
            if type(parity) is not str:
                raise InvalidInput('Option parity must be of type string.')
            parity = parity.lower()
            if parity != 'call' and parity != 'put':
                raise InvalidInput('Option parity must be \"call\" or \"put\".')
            self.parity = parity

        ## spot price
        if 'spot' in args:
            spot = args['spot']
            if type(spot) is not int and type(spot) is not float:
                raise InvalidInput('Spot price must be of type int or float.')
            if spot < 0:
                raise InvalidInput('Spot price must be a non-negative number.')
            self.spot = spot * 1.0

        ## strike price
        if 'strike' in args:
            strike = args['strike']
            if type(strike) is not int and type(strike) is not float:
                raise InvalidInput('Strike price must be of type int or float.')
            if strike < 0:
                raise InvalidInput('Strike price must be a non-negative number.')
            self.strike = strike * 1.0

        ## risk-free rate
        if 'intRate' in args:
            intRate = args['intRate']
            if type(intRate) is not int and type(intRate) is not float:
                raise InvalidInput('Interest rate must be of type int or float.')
            self.intRate = intRate * 1.0

        ## dividend yield (i.e. convenience yield or carrying cost)
        if 'divYield' in args:
            divYield = args['divYield']
            if type(divYield) is not int and type(divYield) is not float:
                raise InvalidInput('Dividend yield must be of type int or float.')
            self.divYield = divYield * 1.0

        ## volatility
        if 'vol' in args:
            vol = args['vol']
            if type(vol) is not int and type(vol) is not float:
                raise InvalidInput('Volatility must be of type int or float.')
            self.vol = vol * 1.0
            if vol < 0:
                raise InvalidInput('Volatility must be a non-negative number.')
            self.vol = vol * 1.0

        ## option price
        if 'optionPrice' in args:
            optionPrice = args['optionPrice']
            if type(optionPrice) is not int and type(optionPrice) is not float:
                raise InvalidInput('Option price must be of type int or float.')
            if optionPrice < 0:
                raise InvalidInput('Option price must be a non-negative number.')
            self.optionPrice = optionPrice * 1.0

        ## time-to-maturity vs. expiration date
        if 'timeToMat' in args and 'expireDate' in args:
            raise InvalidInput('Time-to-maturity and expiration date cannot both be specified.')

        ## time-to-maturity
        if 'timeToMat' in args:
            timeToMat = args['timeToMat']
            if type(timeToMat) is not int and type(timeToMat) is not float:
                raise InvalidInput('Time-to-maturity must be of type int or float.')
            if timeToMat < 0:
                raise InvalidInput('Time-to-maturity must be a non-negative number.')
            self.timeToMat = timeToMat * 1.0

        ## expiration date
        if 'expireDate' in args:
            expireString = args['expireDate']
            if type(expireString) is not str:
                raise InvalidInput('Expiration date must be of type string.')
            expireDate = None
            validDateTypes = ["%m/%d/%Y", "%m %d %Y", "%m-%d-%Y", "%m.%d.%Y", \
                                "%Y/%m/%d", "%Y %m %d", "%Y-%m-%d", "%Y.%m.%d", \
                                "%b %d,%Y", "%b %d, %Y", "%b %d %Y", "%b-%d-%Y", \
                                "%B %d,%Y", "%B %d, %Y", "%B %d %Y", "%B-%d-%Y"]
            for dateType in validDateTypes:
                try:
                    expireDate = datetime.strptime(expireString, dateType).date()
                except:
                    pass
                if expireDate is not None:
                    break
            if expireDate is None:
                raise InvalidInput('Expiration date must take one of the formats: \"' + \
                                    '\", \"'.join(validDateTypes) + '\".')
            if expireDate <= date.today():
                raise InvalidInput('Expiration date must be after today.')
            ### calculate time-to-maturity
            self.timeToMat = self._calculateTimeToMat(expireDate) / self.volDays


    def _checkParams(self, paramList):
        paramDict = {'self.parity': self.parity,
                     'self.spot': self.spot,
                     'self.strike': self.strike,
                     'self.intRate': self.intRate,
                     'self.divYield': self.divYield,
                     'self.vol': self.vol,
                     'self.optionPrice': self.optionPrice,
                     'self.timeToMat': self.timeToMat}

        for paramString in paramList:
            if paramDict[paramString] is None:
                raise MissingInput('Missing {}.'.format(paramString[5:]))

    def _calculateTimeToMat(self, expireDate):
        # Monday counts as 1.25 vol days
        # Saturday/Sunday counts as 0 vol days

        calendarDays = (expireDate - date.today()).days
        volDays = 5.25 * int(calendarDays / 7.0)

        tempDate = expireDate - timedelta(calendarDays % 7.0 + 1)
        while tempDate <= expireDate:
            if tempDate.weekday() == 0:
                volDays += 1.25
            elif tempDate.weekday() < 5:
                volDays += 1
            tempDate += timedelta(days=1)

        return volDays

class InvalidInput(Exception):
    pass

class MissingInput(Exception):
    pass


