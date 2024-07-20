def presentVal(futureVal, discountRate, periods):
    return futureVal / (1 + discountRate) ** periods

def futureVal(presentVal, discountRate, periods):
    return presentVal * (1 + discountRate) ** periods

def netPresentVal(discountRate, cashflows):
    totalVal = 0.0

    for index, cashflow in enumerate(cashflows):
        totalVal += cashflow / (1 + discountRate) ** index

    return totalVal

def presentValPerpetuity(cashflow, discountRate):
    return cashflow / discountRate

def presentValPerpetuityDue(cashflow, discountRate):
    return cashflow / discountRate * (1 + discountRate)

def presentValAnnuity(cashflow, discountRate, periods):
    return cashflow / discountRate * (1 - 1 / (1 + discountRate) ** periods)

def presentValAnnuityDue(cashflow, discountRate, periods):
    return cashflow / discountRate * (1 - 1 / (1 + discountRate) ** periods) * (1 + discountRate)

def presentValGrowingAnnuity(cashflow, discountRate, periods, growthRate):
    return cashflow / discountRate * (1 - (1 + growthRate) ** periods / (1 + discountRate) ** periods)

def futureValAnnuity(cashflow, discountRate, periods):
    return cashflow / discountRate * ((1 + discountRate) ** periods - 1)

def futureValAnnuityDue(cashflow, discountRate, periods):
    return cashflow / discountRate * ((1 + discountRate) ** periods - 1) * (1 + discountRate)

def effectiveAnnualRate(apr, frequency):
    return (1 + apr / frequency) ** frequency - 1

def stockEvaluation(discountRate, ltGrowthRate, dividends):
    divArray = dividends[:-1]
    divLast = dividends[-1]

    numPeriods = len(dividends) - 1

    presVal = netPresentVal(discountRate, divArray) * (1 + discountRate)

    lastDiv = divLast / (discountRate - ltGrowthRate)

    totalVal = presVal + presentVal(lastDiv, discountRate, numPeriods)

    return totalVal

def dividendDiscountModel(discountRate, dividends, growthRate, stockPrice, periods):
    totalCashflows = 0

    for period in range(1, periods + 1):
        growthFactor = (1 + growthRate)
        discountFactor = (1 + discountRate) ** period

        cashflow = (dividends * growthFactor) ** period / discountFactor

        totalCashflows = totalCashflows + cashflow

    terminalVal = stockPrice / (1 + discountRate) ** periods

    return totalCashflows + terminalVal

def gordonGrowthModel(dividend, dividendGrowthRate, requiredRateOfReturn):
    dividendPeriodOne = dividend * (1 + dividendGrowthRate)

    return dividendPeriodOne / (requiredRateOfReturn - dividendGrowthRate)

def multistageGrowthModel(dividend, discountRate, growthRate, constantGrowthRate, periods):
    totalVal = 0

    for period in range(1, periods + 1):
        if period == periods:
            terminalDividend = (dividend * (1 + growthRate) ** period)
            terminalVal = terminalDividend / (discountRate - constantGrowthRate)
            terminalValDiscount = terminalVal / (1 + discountRate) ** (period - 1)
            totalVal += terminalValDiscount
        else:
            cashflow = (dividend * (1 + growthRate) ** period) / (1 + discountRate) ** period
            totalVal += cashflow

    return totalVal

def preferredStockValuation(dividend, requiredRateOfReturn):
    return dividend / requiredRateOfReturn

