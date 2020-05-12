# this file is for variables
from random import randint

import fun
import screen
import random
import pandas as pd

#some important var
turbine_radius = 55
turbine_efficiencyfactor = 0.4
turbinecapacity = 3
airdensity = 1.2

max_possible_bid = 100

#if this number is zero then it calculates with projects which are too expensive as not being built
ifmax_thenmax = 1

#Creates basic variables
def changable_var():
    global no_projects
    no_projects = screen.EnterField

    global density_min
    global density_max
    density_min = screen.EnterField
    density_max = screen.EnterField


    """tohle ted nefunguje protoze je to pocitane od LCOE base nize a prepocitavane korekcnim mechanismem podle EEG"""
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


pdf_options = ["random", "beta", "gauss", "linear", "beta_lin", "gauss_lin"]
pdf_functions = {"random": lambda: fun.ran_gen(lowerlimit=density_min.var, upperlimit=density_max.var, size=no_projects.var),
                "beta": lambda: fun.beta_function(size=no_projects.var, parameteralfa=pdf_parameter1.var, parameterbeta=pdf_parameter2.var, lowerlimit=density_min.var, upperlimit=density_max.var),
                "gauss": lambda: fun.gauss(size=no_projects.var, lowerlimit=density_min.var, upperlimit=density_max.var),
                "linear": lambda: fun.x_inbetween(size=no_projects.var, lower=density_min.var, upper=density_max.var),
                "beta_lin": lambda: fun.beta_lin(size=no_projects.var, lower=density_min.var, upper=density_max.var, parameteralfa=pdf_parameter1.var, parameterbeta=pdf_parameter2.var),
                "gauss_lin": lambda: fun.gauss_lin(size=no_projects.var, lowerlimit=density_min.var, upperlimit=density_max.var)

                 }

"""
--------------------------------------------------------
"""

#Creates projects

def gen_projects_germ():
    # Generates production
    productions = pdf_functions[str(pdf.picked)]()
    projects["power_density"] = productions


    # Generates LCOE based on production
    projects["production"] = []
    # linear_gen(in_value, in_lower, in_upper, out_lower, out_upper) - intentionaly LCOE max min reversed
    for i in projects["power_density"]:
        projects["production"].append(fun.density_to_production(powerdensity=i, radius=turbine_radius , efficiencyfactor=turbine_efficiencyfactor , turbinecapacity=turbinecapacity))

    projects["estimated_ws"] = []
    for i in projects["production"]:
        projects["estimated_ws"].append(
            fun.density_to_wspeed(production=i, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor,
                                  turbinecapacity=turbinecapacity, airdensity=airdensity))

    projects["site_qual"] = []
    projects["site_qual_corr"] = []
    for i in range(0, no_projects.var):
        x = projects["estimated_ws"][i]/reference_ws
        projects["site_qual"].append(x)

        projects["site_qual_corr"].append(1.0076*(x**(-0.645)))

    projects["LCOE_prod"] = []
    for i in projects["site_qual_corr"]:
        projects["LCOE_prod"].append(LCOE_base * i)

    # Generates other fact factors
    others = fun.ran_int(0, 100, no_projects.var)
    projects["other"] = []
    for i in others:
        x = fun.linear_gen(i, 0, 100, 1 - others_change.var/100, 1 + others_change.var/100)
        projects["other"].append(x)

    # Calculates LCOEs
    projects["LCOE"] = []
    for i in range(0, no_projects.var):
        x = projects["LCOE_prod"][i] * projects["other"][i]
        projects["LCOE"].append(x)

    projects["elprice"] = []
    # Just adds electricity price
    for i in range (0, no_projects.var):
        projects["elprice"].append(el_price.var)

    projects["comp_coef"] = []
    for i in projects["site_qual_corr"]:
        x = max(min(i, correction_max), correction_min)
        projects["comp_coef"].append(x)


        """projects["comp_adjustment"].append(compensation_reference/projects["LCOE_prod"][i])
        x = projects["LCOE_prod"][i] * (1 - projects["comp_adjustment"][i])
        max_comp =  LCOE_min.var / LCOE_max.var
        x = (projects["LCOE_prod"][i] - LCOE_min.var) / (LCOE_max.var - LCOE_min.var) * max_comp
        projects["comp_coef"].append(x)"""

projects_compensation = {}

compensation_scenarios = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
keofnoref = compensation_scenarios.index(0.9)


def compensation_calc():
    cat = ["correction", "extra_comp", "min_bid",  "possible_winner", "too_exp", "winner", "bid_through", "subsidy_min", "subsidy_max", "el_produced", "el_too_exp", "paid_min", "paid_max", "max_poss_bid"]
    for ii in compensation_scenarios:
        projects_compensation[ii] = {}
        for i in cat:
            projects_compensation[ii][i] = []

    for ii in range(0, no_projects.var):
        for i in compensation_scenarios:
            x = (projects["comp_coef"][ii] - 1) * i + 1
            projects_compensation[i]["correction"].append(x)

            projects_compensation[i]["min_bid"].append(round(projects["LCOE"][ii] / projects_compensation[i]["correction"][ii], 3))
            projects_compensation[i]["extra_comp"].append(projects["LCOE"][ii] - projects_compensation[i]["min_bid"][ii])

            projects_compensation[i]["max_poss_bid"].append(max_possible_bid/((correction_max_bid-1) * i + 1))


    # find winning projects
    for i in compensation_scenarios:
        y = fun.Nminelements(projects_compensation[i]["min_bid"], min(winning_projects.var, no_projects.var))
        for ii in range(0, no_projects.var):
            if projects_compensation[i]["min_bid"][ii] > y:
                projects_compensation[i]["possible_winner"].append(0)
            else:
                projects_compensation[i]["possible_winner"].append(1)

    for i in compensation_scenarios:
        below_max = []
        for ii in range(0, no_projects.var):
            if ifmax_thenmax == 1:
                below_max.append(1)

            elif projects_compensation[i]["possible_winner"][ii] * projects_compensation[i]["min_bid"][ii] > max_possible_bid/((correction_max_bid-1) * i + 1):
                below_max.append(0)
            else:
                below_max.append(1)

            projects_compensation[i]["winner"].append(
                projects_compensation[i]["possible_winner"][ii] * below_max[ii])

            projects_compensation[i]["too_exp"].append((1 - below_max[ii]) * projects_compensation[i]["possible_winner"][ii])





    # if winners are equal then it selects winners randomly
    for i in compensation_scenarios:
        if sum(projects_compensation[i]["winner"]) > winning_projects.var:
            indices = [ii for ii, x in enumerate(projects_compensation[i]["winner"]) if x == 1]
            random_winners = random.sample(indices, winning_projects.var)

            for iii in range (0, len(projects_compensation[i]["winner"])):
                projects_compensation[i]["winner"][iii] = 0

            for iii in random_winners:
                projects_compensation[i]["winner"][iii] = 1

        else:
            pass

    for ii in range(0, no_projects.var):
        for i in compensation_scenarios:
            w = projects_compensation[i]["min_bid"][ii] * projects_compensation[i]["winner"][ii]
            projects_compensation[i]["bid_through"].append(w)

            x = min(max(projects_compensation[i]["min_bid"][ii] * projects_compensation[i]["correction"][ii]
                     - projects["elprice"][ii], 0), projects_compensation[i]["max_poss_bid"][ii])
            x = x * projects_compensation[i]["winner"][ii]

            projects_compensation[i]["subsidy_min"].append(x)

            y = projects["production"][ii] * projects_compensation[i]["winner"][ii]
            projects_compensation[i]["el_produced"].append(y)

            z = projects["production"][ii] * projects_compensation[i]["too_exp"][ii]
            projects_compensation[i]["el_too_exp"].append(z)



    for ii in range(0, no_projects.var):
        for i in compensation_scenarios:

            """"compensation_scenarios: [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
                correction_max = 100
                correction_min = -100
                
                max_possible_bid = 100
                correction_max_bid = 1            
            """

            max_possible = max(projects_compensation[i]["bid_through"])
            x = max(projects_compensation[i]["winner"][ii] * (max_possible * projects_compensation[i]["correction"][ii] - projects["elprice"][ii]), 0)

            #if undersubscribed - goes to max
            if sum(projects_compensation[i]["winner"]) < winning_projects.var:
                x = float(projects_compensation[i]["max_poss_bid"][ii] * projects_compensation[i]["correction"][ii] - projects["elprice"][ii])
            else:
                pass

            projects_compensation[i]["subsidy_max"].append(x)


            z = projects_compensation[i]["el_produced"][ii] * projects_compensation[i]["subsidy_min"][ii]
            projects_compensation[i]["paid_min"].append(z)

            w = projects_compensation[i]["el_produced"][ii] * projects_compensation[i]["subsidy_max"][ii]
            projects_compensation[i]["paid_max"].append(w)

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
            "max_poss_bid": []

    }

create_storage_temporary()

def store_data_temporary():
    global storage_temporary

    for i in projects_compensation:
        storage_temporary["density_min"].append(float(density_min.var))
        storage_temporary["density_max"].append(float(density_max.var))
        storage_temporary["LCOE_min"].append(float(LCOE_min.var))
        storage_temporary["LCOE_max"].append(float(LCOE_max.var))
        storage_temporary["reference_ws"].append(float(reference_ws))
        storage_temporary["LCOE_base"].append(float(LCOE_base))
        storage_temporary["pdf"].append(str(pdf.picked))
        storage_temporary["pdf_parameter1"].append(str(pdf_parameter1.var))
        storage_temporary["pdf_parameter2"].append(str(pdf_parameter2.var))
        storage_temporary["supply"].append(float(no_projects.var))
        storage_temporary["demand"].append(float(winning_projects.var))
        storage_temporary["dem_sup"].append(float(winning_projects.var/no_projects.var))
        storage_temporary["other_factors"].append(float(others_change.var))
        storage_temporary["el_prices"].append(float(el_price.var))
        storage_temporary["compensation"].append(float(i))
        storage_temporary["el_produced"].append(sum(projects_compensation[i]["el_produced"]))
        storage_temporary["el_too_exp"].append(sum(projects_compensation[i]["el_too_exp"]))
        storage_temporary["paid_min"].append(sum(projects_compensation[i]["paid_min"]))
        storage_temporary["paid_max"].append(sum(projects_compensation[i]["paid_max"]))
        storage_temporary["subsidy_min"].append(sum((projects_compensation[i]["paid_min"])/sum(projects_compensation[i]["el_produced"])))
        storage_temporary["subsidy_max"].append(float(sum((projects_compensation[i]["paid_max"])/sum(projects_compensation[i]["el_produced"]))))

        lowest_index = projects_compensation[i]["min_bid"].index(min(projects_compensation[i]["min_bid"]))
        storage_temporary["auction_bid_min_succ"].append(projects_compensation[i]["bid_through"][lowest_index])
        storage_temporary["auction_bid_max_succ"].append(max(projects_compensation[i]["bid_through"]))
        storage_temporary["auction_bid_max_received"].append(max(projects_compensation[i]["min_bid"]))

        storage_temporary["max_poss_bid"].append(sum(projects_compensation[i]["max_poss_bid"])/len(projects_compensation[i]["max_poss_bid"]))


df_storage = pd.DataFrame()
def store_data():
    storage_temporary_tobeappended = pd.DataFrame.from_dict(storage_temporary, orient='index').transpose()
    storage_temporary_tobeappended = storage_temporary_tobeappended.groupby(["compensation"]).apply(lambda x: x.mean())

    for i in ["pdf", "pdf_parameter1", "pdf_parameter2"]:
        storage_temporary_tobeappended[i] = storage_temporary[i][0]

    global df_storage
    df_storage = df_storage.append(storage_temporary_tobeappended)
    df_storage = df_storage.reset_index(drop=True)


def do_the_calc_germ():
    gen_projects_germ()
    compensation_calc()
    store_data_temporary()





""" Normal non german calc below -----------------------------------  """
def gen_projects():
    # Generates production
    productions = pdf_functions[str(pdf.picked)]()
    projects["power_density"] = productions


    # Generates LCOE based on production
    projects["production"] = []
    # linear_gen(in_value, in_lower, in_upper, out_lower, out_upper) - intentionaly LCOE max min reversed
    for i in projects["power_density"]:
        projects["production"].append(fun.density_to_production(powerdensity=i, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor , turbinecapacity=turbinecapacity))

    projects["estimated_ws"] = []
    for i in projects["production"]:
        projects["estimated_ws"].append(
            fun.density_to_wspeed(production=i, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor,
                                  turbinecapacity=turbinecapacity, airdensity=airdensity))

    max_production = fun.density_to_production(powerdensity=density_max.var, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor , turbinecapacity=turbinecapacity)
    min_production = fun.density_to_production(powerdensity=density_min.var, radius=turbine_radius, efficiencyfactor=turbine_efficiencyfactor,  turbinecapacity=turbinecapacity)

    projects["site_qual"] = []

    for i in range(0, no_projects.var):
        x = (projects["production"][i] - min_production)/(max_production - min_production)
        projects["site_qual"].append(x)

    projects["LCOE_prod"] = []
    for i in range(0, no_projects.var):
        projects["LCOE_prod"].append(LCOE_max.var - projects["site_qual"][i] * (LCOE_max.var - LCOE_min.var))


    projects["site_qual_corr"] = []
    for i in range(0, no_projects.var):
        x = projects["LCOE_prod"][i] / compensation_reference
        projects["site_qual_corr"].append(x)

    # Generates other fact factors
    others = fun.ran_int(0, 100, no_projects.var)
    projects["other"] = []
    for i in others:
        x = fun.linear_gen(i, 0, 100, 1 - others_change.var/100, 1 + others_change.var/100)
        projects["other"].append(x)

    # Calculates LCOEs
    projects["LCOE"] = []
    for i in range(0, no_projects.var):
        x = projects["LCOE_prod"][i] * projects["other"][i]
        projects["LCOE"].append(x)

    projects["elprice"] = []
    # Just adds electricity price
    for i in range(0, no_projects.var):
        projects["elprice"].append(el_price.var)

    projects["comp_coef"] = []
    for i in projects["site_qual_corr"]:
        x = max(min(i, correction_max), correction_min)
        projects["comp_coef"].append(x)


def do_the_calc():
    gen_projects()
    compensation_calc()
    store_data_temporary()





