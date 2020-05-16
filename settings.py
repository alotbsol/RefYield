# this file is for variables
import random
from random import randint
import fun
import screen
import pandas as pd

#some important var
turbine_radius = 55
turbine_efficiencyfactor = 0.4
turbinecapacity = 3
airdensity = 1.2

max_possible_bid = 100

#if this number is zero then it calculates with projects which are too expensive as not being built
ifmax_thenmax = 0

#Creates basic variables
def changable_var():
    global no_projects
    no_projects = screen.EnterField

    global density_min
    global density_max
    density_min = screen.EnterField
    density_max = screen.EnterField


    global LCOE_min
    global LCOE_max
    LCOE_min = screen.EnterField
    LCOE_max = screen.EnterField

    global LCOE_base
    LCOE_base = 50

    # max change in percentages
    global others_change
    others_change = screen.EnterField

    # max change in percentages
    global el_price
    el_price = screen.EnterField

    # max change in percentages
    global extra_compensation
    extra_compensation = screen.EnterField

    # no of iterations
    global iterations
    iterations = screen.EnterField


def create_variables():
    global compensation_level
    compensation_level = 0

    global compensation_reference
    compensation_reference = 50

    global reference_ws
    reference_ws = 6.45

    global site_qual_min
    global site_qual_max

    """production"""
    x_prod = fun.density_to_production(powerdensity=density_min.var, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor,
                              turbinecapacity=turbinecapacity)
    """windspeed"""
    x_speed = fun.density_to_wspeed(production=x_prod, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor,
                          turbinecapacity=turbinecapacity, airdensity=airdensity)

    site_qual_min = x_speed/reference_ws

    """production"""
    x_prod = fun.density_to_production(powerdensity=density_max.var, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor,
                              turbinecapacity=turbinecapacity)
    """windspeed"""
    x_speed = fun.density_to_wspeed(production=x_prod, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor,
                          turbinecapacity=turbinecapacity, airdensity=airdensity)


    site_qual_max = x_speed/reference_ws

    global correction_max
    global correction_min
    global correction_max_bid
    correction_max = 100
    correction_min = -100
    correction_max_bid = 1


    global projects
    projects = {
        "power_density": [],
        "estimated_ws": [],
        "site_qual": [],
        "site_qual_corr": [],
        "production": [],
        "LCOE_prod": [],
        "other": [],
        "LCOE": [],
        "elprice": [],
        
        "comp_coef": [],
    }


#Other variables entry field
pdf = "hmmm"
pdf_parameter1 = screen.EnterField
pdf_parameter2 = screen.EnterField
winning_projects = screen.EnterField


#different probability density functions and number generation
pdf_options = ["random", "beta", "gauss", "linear", "beta_lin", "gauss_lin"]
pdf_functions = {"random": lambda: fun.ran_gen(lowerlimit=density_min.var, upperlimit=density_max.var, size=no_projects.var),
                "beta": lambda: fun.beta_function(size=no_projects.var, parameteralfa=pdf_parameter1.var, parameterbeta=pdf_parameter2.var, lowerlimit=density_min.var, upperlimit=density_max.var),
                "gauss": lambda: fun.gauss(size=no_projects.var, lowerlimit=density_min.var, upperlimit=density_max.var),
                "linear": lambda: fun.x_inbetween(size=no_projects.var, lower=density_min.var, upper=density_max.var),
                "beta_lin": lambda: fun.beta_lin(size=no_projects.var, lower=density_min.var, upper=density_max.var, parameteralfa=pdf_parameter1.var, parameterbeta=pdf_parameter2.var),
                "gauss_lin": lambda: fun.gauss_lin(size=no_projects.var, lowerlimit=density_min.var, upperlimit=density_max.var)

                 }

# variables which sets difference scenarios of reference yield mechanism
projects_compensation = {}
compensation_scenarios = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
keofnoref = compensation_scenarios.index(0.9)

#creates temporary storage
def create_storage_temporary():
    global storage_temporary
    storage_temporary = {
            "density_min": [],
            "density_max": [],
            "LCOE_min": [],
            "LCOE_max": [],
            "reference_ws": [],
            "LCOE_base": [],
            "pdf": [],
            "pdf_parameter1": [],
            "pdf_parameter2": [],
            "supply": [],
            "demand": [],
            "dem_sup": [],
            "other_factors": [],
            "el_prices": [],
            "compensation": [],
            "el_produced": [],
            "el_too_exp": [],
            "paid_min": [],
            "paid_max": [],
            "subsidy_min": [],
            "subsidy_max": [],
            "auction_bid_min_succ": [],
            "auction_bid_max_succ": [],
            "auction_bid_max_received": [],
            "max_poss_bid": [],
            "same_winners": [],
            "same_marginal_project": []

    }


create_storage_temporary()


#creates pandas dataframe for longterm storage
df_storage = pd.DataFrame()



