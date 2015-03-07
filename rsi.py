# A very simple algorithm that buys and sells based on a calculated RSI value for a given stock (Relative Strength Index)
# RSI = 100-100/(1+RS*) where RS* = avg(total gains)/avg(total losses)

import pandas as pd
import numpy as np

def initialize(context):
    context.security = symbol('AAPL')

def handle_data(context, data):
    
    # Get the prices from the past 6 months (about 120 trading days)
    
    price_history = history(bar_count=120, frequency="1d", field = "price")
    # log.debug(price_history)
    
    # These variables will keep track of our total gains and losses so far within the loop
    
    gains = 0
    losses = 0
    
    # This loop will traverse the array from current day to 120 days back, 1 day at a time
    for x in range(-1,-120,-1):
        # If current price is positive, assign it to current_gain and add it to our gains variable
        # If its negative, do the latter
        zero = float(0)
        
        current_price = float(price_history[context.security][x])
        print "current price"
        print current_price
        
        price_change = float(current_price - price_history[context.security][x+1])
        print "price change"
        print price_change
        
        if price_change > zero:
            
            current_gain = price_change
            current_loss = 0
            gains += price_change
            
        if price_change < zero:
            
            current_loss = price_change
            current_gain = 0
            losses += price_change
            
        # Calculate average gain and loss thus far by dividing total gains or total losses by number of days passed
        current_avg_gain = ((gains)/x)
        current_avg_loss = ((losses)/x)
        
        # Average overall gain/loss overall is calculated by ((prev gain or loss)*(x-1)+current gain or loss)/x
        avg_gain_overall = ((current_avg_gain)*(x-1)+current_gain)/x
        print "AVG gain"
        print avg_gain_overall
        avg_loss_overall = ((current_avg_loss)*(x-1)+current_loss)/x
        print "AVG loss"
        print avg_loss_overall
        
        # We can calculate our RSI value b using the equation 100-100/(1+RS) where RS is average of x days' up closes divided
        # by avg of x days' down closes
        
        RS = avg_gain_overall/avg_loss_overall
        print "RS"
        print RS
        
        RSI = 100-100/(1+RS)
        print "RSI"
        print RSI

        # If our RSI is 30 or below, we buy, it is oversold. If >= 70, sell.
    
        if RSI <= 30:
            curr_price = data[context.security].price
            cash = context.portfolio.cash
    
            num_shares = int(cash/curr_price)
            order(context.security, +num_shares)
            #log.info("Buying %s" % (context.security.symbol))
        
        if RSI >= 70:
            curr_price = data[context.security].price
            cash = context.portfolio.cash
    
            num_shares = int(cash/curr_price)
            order(context.security, 0)
            #log.info("Sold all shares of %s" % (context.security.symbol))
        
    record(portfolio_value=context.portfolio.portfolio_value)
