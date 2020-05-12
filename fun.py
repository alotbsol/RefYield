# this file is for functions
from numpy.random import randint
import numpy as np
from scipy.stats import beta
from scipy.stats import norm
from scipy.stats import truncnorm
from math import pi

import settings

#average function
def average(lst):
    return sum(lst) / len(lst)


#Random generation of x numbers
def ran_gen(lowerlimit, upperlimit, size):
    x = np.random.uniform(int(lowerlimit), int(upperlimit), int(size))
    return list(x)

def ran_gen_float(lowerlimit, upperlimit, size):
    x = np.random.uniform(lowerlimit, upperlimit, int(size))
    return list(x)

def ran_int(lowerlimit, upperlimit, size):
    return list(randint(lowerlimit, upperlimit + 1, size))


#Beta generation
def beta_function(size, parameteralfa, parameterbeta, lowerlimit, upperlimit):
    x = np.random.beta(parameteralfa, parameterbeta, int(size))
    y = (int(upperlimit) - int(lowerlimit)) * x + int(lowerlimit)
    return list(y)

#normal generation
def gauss(size, lowerlimit, upperlimit):
    generation_list = ran_gen_float(lowerlimit=0.01, upperlimit=0.99, size=size)
    x = []
    for i in generation_list:
        x.append(norm.ppf(i))

    x = [(1-(norm.ppf(0.99) - i)/(norm.ppf(0.99)-norm.ppf(0.01))) for i in x]
    x = [i * (upperlimit - lowerlimit) + lowerlimit for i in x]

    return list(x)


#Converts value to different list - linear
def linear_gen(in_value, in_lower, in_upper, out_lower, out_upper):
    in_spread = in_upper - in_lower
    in_proportion = in_value - in_lower
    out_spread = out_upper - out_lower

    out_val = in_proportion/in_spread * out_spread + out_lower
    return out_val

#returns x numbers inbetween - linspace
def x_inbetween(lower, upper, size):
    x = np.linspace(start=lower, stop=upper, num=size, endpoint=True, retstep=False, dtype=None, axis=0)
    return list(x)

#linspaced beta
def beta_lin(lower, upper, parameteralfa, parameterbeta, size):
    generation_list = x_inbetween(0, 1, size)
    x = []
    for i in generation_list:
        x.append(beta.ppf(i, parameteralfa, parameterbeta))

    x = [i * (upper - lower) + lower for i in x]

    return list(x)

#linspaced gauss
def gauss_lin(size, lowerlimit, upperlimit):
    generation_list = x_inbetween(0.01, 0.99, size)

    x = []
    for i in generation_list:
        x.append(norm.ppf(i))

    x = [(1-(norm.ppf(0.99) - i)/(norm.ppf(0.99)-norm.ppf(0.01))) for i in x]
    x = [i * (upperlimit - lowerlimit) + lowerlimit for i in x]

    return list(x)

#returns x lowest elements in a list
def Nminelements(inputlist, N):
    winners_list = []
    copylist =list(inputlist)

    for i in range(0, N):
        min1 = copylist[0]
        for j in range(len(copylist)):
            if copylist[j] < min1:
                min1 = copylist[j];
        copylist.remove(min1);
        winners_list.append(min1)

    lastwinner = max(winners_list)
    return lastwinner

# converts power density to production in MWh
def density_to_production(powerdensity, radius, efficiencyfactor, turbinecapacity):
    """ https://rechneronline.de/wind-power/ """
    x = pi/2 * (radius**2) * efficiencyfactor * powerdensity /1000000
    toMWhperMW = 24 * 365 / turbinecapacity
    return (x * toMWhperMW)

# converts power density to wind speed
def density_to_wspeed(production, radius, efficiencyfactor, turbinecapacity, airdensity):
    """ https://rechneronline.de/wind-power/ """
    windspeed = (production / (24 * 365 / turbinecapacity))/(pi/2 * (radius**2) * airdensity * efficiencyfactor /1000000)**(1/3)
    return (windspeed)

# converts wind speed to production - not in use
def wind_to_production(windspeed, radius, airdensity, efficiencyfactor, turbinecapacity):
    """ https://rechneronline.de/wind-power/ """
    x = pi/2 * (radius**2) * (windspeed ** 3) * airdensity * efficiencyfactor /1000000
    toMWh = 24 * 365 / turbinecapacity
    return (x * toMWh)

