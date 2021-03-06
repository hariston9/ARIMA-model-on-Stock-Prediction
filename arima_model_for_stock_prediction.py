# -*- coding: utf-8 -*-
"""ARIMA Model for Stock prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iD2CWJg4te5acJ13nTQVyczXIfDeFRw1

ARIMA aito regressive Integrated Moving average is a forecasting algorithm based on the idea that the information in the past values of the time series can alone be used to predict the future values

ARIMA models explain a time series based on its own past values, basically its own lands and the lagged forcast errors

ARIMA (Auto Regressive Integrated Moving Average) is a forecasting algorithm based on the idea that the information in the past values of the time series can alone be used to predict the future values.

ARIMA models explain a time series based on its own past values, basically its own lags and the lagged forecast errors.

An ARIMA model is characterized by 3 terms p, d, q:
- p is the order of the AR term
- d is the number of differencing required to make the time series stationary
- q is the order of the MA term

As we see in the parameters required by the model, any stationary time series can be modeled with ARIMA models.

Let's explain the term Auto Regressive in ARIMA. It means the model is a linear regression that uses its own lags as predictors. Linear regression models, as we know, work best when the predictors are independent of each other. Otherwise we run into multicollinearity issues where the regression becomes unstable due to correlation.

Now most price series are non stationary otherwise we would all be rich by just buying low and selling high, waiting for the prices to mean revert.
So in order to make ARIMA models work we need to difference it, in this case to compute the returns as they usually randomly distribute around a 0 mean.

So we need to simply subtract the previous value from the current value. Now if we just difference once, we might not get a stationary series so we might need to do that multiple times. 

And the minimum number of differencing operations needed to make the series stationary needs to be imputed into our ARIMA model. If the time series is already stationary, then d is 0. But in stock price forecasting it's almost never 0.

p is the order of the Auto Regressive (AR) term. It refers to the number of lags to be used as predictors. 
q is the order of the Moving Average (MA) term. It refers to the number of lagged forecast errors that should go into the ARIMA Model.

We'll use the Augmented Dickey Fuller (ADF) test to check if the price series is stationary.

The null hypothesis of the ADF test is that the time series is non-stationary. So, if the p-value of the test is less than the significance level (0.05) then we can reject the null hypothesis and infer that the time series is indeed stationary.

So, in our case, if the p-value is greater than 0.05 we'll need to find the order of differencing.

So how to determine the right order of differencing?

The right order of differencing is the minimum differencing required to get a near-stationary series which roams around a defined mean and the Autocorrelation Function plot reaches zero fairly quick.
"""

!pip install ipython

!pip install ipython
import IPython

!pip install nb_black

# Commented out IPython magic to ensure Python compatibility.
from IPython.core.debugger import set_trace

#%load_ext nb_black

import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time

plt.style.use(style="seaborn")
# %matplotlib inline

#df=pd.read_csv

!pip install yfinance

# Load the data set
import yfinance as yf
df = yf.download("GOOG", start="2019-06-03", end="2019-12-17")

df.head(5)

df=df[["Close"]].copy()

df.describe()

"""An ARIMA model is characterised by 3 term (p,d,q):
*p is the oerder of the AR term
* d is the  number of differencing required to make the time series stationary
* q is the order of the MA term

Stationarity and  ADF test

"""

!pip install statsmodels

# Check if price series is staionary
from statsmodels.tsa.stattools import adfuller
result=adfuller(df.Close.dropna())
print(f"ADF Statistic: {result[0]}")
print(f"p-value:{result[0]}")

"""Autocorrelation Function (ACF)"""

from statsmodels.graphics.tsaplots import plot_acf

fig, (ax1 , ax2) = plt.subplots(1,2, figsize=(16,4))

ax1.plot(df.Close)
ax1.set_title("Original")

#add; at the end of the plot function so that the plot is not duplicated
plot_acf(df.Close, ax=ax2);

diff = df.Close.diff().dropna()

fig, (ax1 , ax2) = plt.subplots(1,2, figsize=(16,4))

ax1.plot(diff)
ax1.set_title("Difference Once")

#add; at the end of the plot function so that the plot is not duplicated
plot_acf(diff, ax=ax2);

diff = df.Close.diff().diff().dropna()

fig, (ax1 , ax2) = plt.subplots(1,2, figsize=(16,4))

ax1.plot(diff)
ax1.set_title("Difference twice")

#add; at the end of the plot function so that the plot is not duplicated
plot_acf(diff, ax=ax2);

!pip install pmdarima

# we can use the pmdarima package to get the number of differencing
#! pip install --skip-lock pmdarima
from pmdarima.arima.utils import ndiffs

#!pip3 install --user scipy==1.2.0

#!pip install scipy

import pmdarima

"""p

p is the order of the Auto Regressive(AR) term. It refers to the number of lags to be used as predictors.

We can find out the required number of AR terms by inspecting the Partial Autocorrelation( PACF) plot.

The partial autocorrealtion represents the correlation between the series and its lags
"""

from statsmodels.graphics.tsaplots import plot_acf

diff = df.Close.diff().dropna()

fig, (ax1 , ax2) = plt.subplots(1,2, figsize=(16,4))

ax1.plot(diff)
ax1.set_title("Difference once")
ax2.set_ylim(0,1)
plot_acf(diff, ax=ax2);

"""q

q is the order of the Moving Average(MA) term. It refers to the number of lagged forecase errors that should go into the ARIMA Model.

We can look at the ACF plot for the number of MA terms.
"""

diff = df.Close.diff().dropna()

fig, (ax1 , ax2) = plt.subplots(1,2, figsize=(16,4))

ax1.plot(diff)
ax1.set_title("Difference once")
ax2.set_ylim(0,1)
plot_acf(diff, ax=ax2);

"""Fitting the ARIMA model"""

df

import statsmodels.tsa.arima.model as stats

!pip install statsmodels --upgrade

#from statsmodels.tsa.arima_model import ARIMA

# ARIMA MODEL

model = stats.ARIMA(df.Close, order=(6, 1, 3))
#model_fit = model.fit()

#model= ARIMA(df.Close, order=(6,1,3))
#result= model.fit(disp=0)
result= model.fit()

print(result.summary())

# Plot residual errors
residuals=pd.DataFrame(result.resid)

fig, (ax1, ax2)= plt.subplots(1,2, figsize=(16,4))

ax1.plot(residuals)
ax2.hist(residuals, density=True)

result

#Actual vs Fitted
result.plot_predict(
    start=1,
    end=60,
    dynamic=False,
)

n=int(len(df)*0.8)

train=df.Close[:n]
test=df.Close[n:]

print(len(train))
print(len(test))

import statsmodels.tsa.arima.model as stats
model = stats.ARIMA(train, order=(6, 1, 3))
#model_fit = model.fit()

#model= ARIMA(train, order=(6,1,3))
#result= model.fit(disp=0)
result= model.fit()

result.summary()

step=30

fc, se, conf = result.forecast(step)

fc=pd.Series(fc, index=test[:step].index)
lower=pd.Series(conf[:,0], index=test[:step].index)
upper=pd.Series(conf[:,1], index=test[:step].index)

plt.figure(figsize=(16,8))
plt.plot(test[:step], label="actual")
plt.plot(fc, label="forecast")
plt.fill_between(lower.index, lower, upper, color="k", alpha=0.1)
plt.title("Forecase vs Actual")
plt.legend(loc="upper left")