#Creates projects

import settings
import fun
import pandas as pd


# Generates projects based on EEG reference zield logic, i.e. from base LCOE adjusted bz reference yield model
def gen_projects_germ():
    # Generates production
    productions = settings.pdf_functions[str(settings.pdf.picked)]()
    settings.projects["power_density"] = productions

    # Generates LCOE based on production
    settings.projects["production"] = []
    # linear_gen(in_value, in_lower, in_upper, out_lower, out_upper) - intentionaly LCOE max min reversed
    for i in settings.projects["power_density"]:
        settings.projects["production"].append(fun.density_to_production(powerdensity=i, radius=settings.turbine_radius , efficiencyfactor=settings.turbine_efficiencyfactor , turbinecapacity=settings.turbinecapacity))

    settings.projects["estimated_ws"] = []
    for i in settings.projects["production"]:
        settings.projects["estimated_ws"].append(
            fun.density_to_wspeed(production=i, radius=settings.turbine_radius, efficiencyfactor=settings.turbine_efficiencyfactor,
                                  turbinecapacity=settings.turbinecapacity, airdensity=settings.airdensity))

    settings.projects["site_qual"] = []
    settings.projects["site_qual_corr"] = []
    for i in range(0, settings.no_projects.var):
        x = settings.projects["estimated_ws"][i]/settings.reference_ws
        settings.projects["site_qual"].append(x)

        settings.projects["site_qual_corr"].append(1.0076*(x**(-0.645)))

    settings.projects["LCOE_prod"] = []
    for i in settings.projects["site_qual_corr"]:
        settings.projects["LCOE_prod"].append(settings.LCOE_base * i)

    # Generates other fact factors
    others = fun.ran_int(0, 100, settings.no_projects.var)
    settings.projects["other"] = []
    for i in others:
        x = fun.linear_gen(i, 0, 100, 1 - settings.others_change.var/100, 1 + settings.others_change.var/100)
        settings.projects["other"].append(x)

    # Calculates LCOEs
    settings.projects["LCOE"] = []
    for i in range(0, settings.no_projects.var):
        x = settings.projects["LCOE_prod"][i] * settings.projects["other"][i]
        settings.projects["LCOE"].append(x)

    settings.projects["elprice"] = []
    # Just adds electricity price
    for i in range (0, settings.no_projects.var):
        settings.projects["elprice"].append(settings.el_price.var)

    settings.projects["comp_coef"] = []
    for i in settings.projects["site_qual_corr"]:
        x = max(min(i, settings.correction_max), settings.correction_min)
        settings.projects["comp_coef"].append(x)


# Generates projects based on general logic of min and max LCOE,
def gen_projects():
    # Generates production
    productions = settings.pdf_functions[str(settings.pdf.picked)]()
    settings.projects["power_density"] = productions


    # Generates LCOE based on production
    settings.projects["production"] = []
    # linear_gen(in_value, in_lower, in_upper, out_lower, out_upper) - intentionaly LCOE max min reversed
    for i in settings.projects["power_density"]:
        settings.projects["production"].append(fun.density_to_production(powerdensity=i, radius=settings.turbine_radius, efficiencyfactor=settings.turbine_efficiencyfactor , turbinecapacity=settings.turbinecapacity))

    settings.projects["estimated_ws"] = []
    for i in settings.projects["production"]:
        settings.projects["estimated_ws"].append(
            fun.density_to_wspeed(production=i, radius=settings.turbine_radius, efficiencyfactor=settings.turbine_efficiencyfactor,
                                  turbinecapacity=settings.turbinecapacity, airdensity=settings.airdensity))

    max_production = fun.density_to_production(powerdensity=settings.density_max.var, radius=settings.turbine_radius, efficiencyfactor=settings.turbine_efficiencyfactor , turbinecapacity=settings.turbinecapacity)
    min_production = fun.density_to_production(powerdensity=settings.density_min.var, radius=settings.turbine_radius, efficiencyfactor=settings.turbine_efficiencyfactor,  turbinecapacity=settings.turbinecapacity)

    settings.projects["site_qual"] = []

    for i in range(0, settings.no_projects.var):
        x = (settings.projects["production"][i] - min_production)/(max_production - min_production)
        settings.projects["site_qual"].append(x)

    settings.projects["LCOE_prod"] = []
    for i in range(0, settings.no_projects.var):
        settings.projects["LCOE_prod"].append(settings.LCOE_max.var - settings.projects["site_qual"][i] * (settings.LCOE_max.var - settings.LCOE_min.var))


    settings.projects["site_qual_corr"] = []
    for i in range(0, settings.no_projects.var):
        x = settings.projects["LCOE_prod"][i] / settings.compensation_reference
        settings.projects["site_qual_corr"].append(x)

    # Generates other fact factors
    others = fun.ran_int(0, 100, settings.no_projects.var)
    settings.projects["other"] = []
    for i in others:
        x = fun.linear_gen(i, 0, 100, 1 - settings.others_change.var/100, 1 + settings.others_change.var/100)
        settings.projects["other"].append(x)

    # Calculates LCOEs
    settings.projects["LCOE"] = []
    for i in range(0, settings.no_projects.var):
        x = settings.projects["LCOE_prod"][i] * settings.projects["other"][i]
        settings.projects["LCOE"].append(x)

    settings.projects["elprice"] = []
    # Just adds electricity price
    for i in range(0, settings.no_projects.var):
        settings.projects["elprice"].append(settings.el_price.var)

    settings.projects["comp_coef"] = []
    for i in settings.projects["site_qual_corr"]:
        x = max(min(i, settings.correction_max), settings.correction_min)
        settings.projects["comp_coef"].append(x)


# Based on generated projects calculates results with different degree of reference yield mechanism
def compensation_calc():
    cat = ["correction", "extra_comp", "min_bid",  "possible_winner", "too_exp", "winner", "bid_through", "subsidy_min", "subsidy_max", "el_produced", "el_too_exp", "paid_min", "paid_max", "max_poss_bid"]
    for ii in settings.compensation_scenarios:
        settings.projects_compensation[ii] = {}
        for i in cat:
            settings.projects_compensation[ii][i] = []

    for ii in range(0, settings.no_projects.var):
        for i in settings.compensation_scenarios:
            x = (settings.projects["comp_coef"][ii] - 1) * i + 1
            settings.projects_compensation[i]["correction"].append(x)

            settings.projects_compensation[i]["min_bid"].append(round(settings.projects["LCOE"][ii] / settings.projects_compensation[i]["correction"][ii], 3))
            settings.projects_compensation[i]["extra_comp"].append(settings.projects["LCOE"][ii] - settings.projects_compensation[i]["min_bid"][ii])

            settings.projects_compensation[i]["max_poss_bid"].append(settings.max_possible_bid/((settings.correction_max_bid-1) * i + 1))


    # find winning projects
    for i in settings.compensation_scenarios:
        y = fun.Nminelements(settings.projects_compensation[i]["min_bid"], min(settings.winning_projects.var, settings.no_projects.var))
        for ii in range(0, settings.no_projects.var):
            if settings.projects_compensation[i]["min_bid"][ii] > y:
                settings.projects_compensation[i]["possible_winner"].append(0)
            else:
                settings.projects_compensation[i]["possible_winner"].append(1)

    for i in settings.compensation_scenarios:
        below_max = []
        for ii in range(0, settings.no_projects.var):
            if settings.ifmax_thenmax == 1:
                below_max.append(1)

            elif settings.projects_compensation[i]["possible_winner"][ii] * settings.projects_compensation[i]["min_bid"][ii] > settings.max_possible_bid/((settings.correction_max_bid-1) * i + 1):
                below_max.append(0)
            else:
                below_max.append(1)

            settings.projects_compensation[i]["winner"].append(
                settings.projects_compensation[i]["possible_winner"][ii] * below_max[ii])

            settings.projects_compensation[i]["too_exp"].append((1 - below_max[ii]) * settings.projects_compensation[i]["possible_winner"][ii])


    # if winners are equal then it selects winners randomly
    for i in settings.compensation_scenarios:
        if sum(settings.projects_compensation[i]["winner"]) > settings.winning_projects.var:
            indices = [ii for ii, x in enumerate(settings.projects_compensation[i]["winner"]) if x == 1]
            random_winners = settings.random.sample(indices, settings.winning_projects.var)

            for iii in range (0, len(settings.projects_compensation[i]["winner"])):
                settings.projects_compensation[i]["winner"][iii] = 0

            for iii in random_winners:
                settings.projects_compensation[i]["winner"][iii] = 1

        else:
            pass

    for ii in range(0, settings.no_projects.var):
        for i in settings.compensation_scenarios:
            w = settings.projects_compensation[i]["min_bid"][ii] * settings.projects_compensation[i]["winner"][ii]
            settings.projects_compensation[i]["bid_through"].append(w)

            x = min(max(settings.projects_compensation[i]["min_bid"][ii] * settings.projects_compensation[i]["correction"][ii]
                     - settings.projects["elprice"][ii], 0), settings.projects_compensation[i]["max_poss_bid"][ii])
            x = x * settings.projects_compensation[i]["winner"][ii]

            settings.projects_compensation[i]["subsidy_min"].append(x)

            y = settings.projects["production"][ii] * settings.projects_compensation[i]["winner"][ii]
            settings.projects_compensation[i]["el_produced"].append(y)

            z = settings.projects["production"][ii] * settings.projects_compensation[i]["too_exp"][ii]
            settings.projects_compensation[i]["el_too_exp"].append(z)


    for ii in range(0, settings.no_projects.var):
        for i in settings.compensation_scenarios:

            max_possible = max(settings.projects_compensation[i]["bid_through"])
            x = max(settings.projects_compensation[i]["winner"][ii] * (max_possible * settings.projects_compensation[i]["correction"][ii] - settings.projects["elprice"][ii]), 0)

            #if undersubscribed - goes to max
            if sum(settings.projects_compensation[i]["winner"]) < settings.winning_projects.var:
                x = float(settings.projects_compensation[i]["max_poss_bid"][ii] * settings.projects_compensation[i]["correction"][ii] - settings.projects["elprice"][ii])
            else:
                pass

            settings.projects_compensation[i]["subsidy_max"].append(x)


            z = settings.projects_compensation[i]["el_produced"][ii] * settings.projects_compensation[i]["subsidy_min"][ii]
            settings.projects_compensation[i]["paid_min"].append(z)

            w = settings.projects_compensation[i]["el_produced"][ii] * settings.projects_compensation[i]["subsidy_max"][ii]
            settings.projects_compensation[i]["paid_max"].append(w)


# Stores all data of rounds/itterations for further use
def store_data_temporary():
    global storage_temporary

    for i in settings.projects_compensation:
        settings.storage_temporary["density_min"].append(float(settings.density_min.var))
        settings.storage_temporary["density_max"].append(float(settings.density_max.var))
        settings.storage_temporary["LCOE_min"].append(float(settings.LCOE_min.var))
        settings.storage_temporary["LCOE_max"].append(float(settings.LCOE_max.var))
        settings.storage_temporary["reference_ws"].append(float(settings.reference_ws))
        settings.storage_temporary["LCOE_base"].append(float(settings.LCOE_base))
        settings.storage_temporary["pdf"].append(str(settings.pdf.picked))
        settings.storage_temporary["pdf_parameter1"].append(str(settings.pdf_parameter1.var))
        settings.storage_temporary["pdf_parameter2"].append(str(settings.pdf_parameter2.var))
        settings.storage_temporary["supply"].append(float(settings.no_projects.var))
        settings.storage_temporary["demand"].append(float(settings.winning_projects.var))
        settings.storage_temporary["dem_sup"].append(float(settings.winning_projects.var/settings.no_projects.var))
        settings.storage_temporary["other_factors"].append(float(settings.others_change.var))
        settings.storage_temporary["el_prices"].append(float(settings.el_price.var))
        settings.storage_temporary["compensation"].append(float(i))
        settings.storage_temporary["el_produced"].append(sum(settings.projects_compensation[i]["el_produced"]))
        settings.storage_temporary["el_too_exp"].append(sum(settings.projects_compensation[i]["el_too_exp"]))
        settings.storage_temporary["paid_min"].append(sum(settings.projects_compensation[i]["paid_min"]))
        settings.storage_temporary["paid_max"].append(sum(settings.projects_compensation[i]["paid_max"]))
        settings.storage_temporary["subsidy_min"].append(sum((settings.projects_compensation[i]["paid_min"])/sum(settings.projects_compensation[i]["el_produced"])))
        settings.storage_temporary["subsidy_max"].append(float(sum((settings.projects_compensation[i]["paid_max"])/sum(settings.projects_compensation[i]["el_produced"]))))

        lowest_index = settings.projects_compensation[i]["min_bid"].index(min(settings.projects_compensation[i]["min_bid"]))
        settings.storage_temporary["auction_bid_min_succ"].append(settings.projects_compensation[i]["bid_through"][lowest_index])
        settings.storage_temporary["auction_bid_max_succ"].append(max(settings.projects_compensation[i]["bid_through"]))
        settings.storage_temporary["auction_bid_max_received"].append(max(settings.projects_compensation[i]["min_bid"]))

        settings.storage_temporary["max_poss_bid"].append(sum(settings.projects_compensation[i]["max_poss_bid"])/len(settings.projects_compensation[i]["max_poss_bid"]))

        x = 0
        for ii in range(0, len(settings.projects_compensation[i]["winner"])):
            if settings.projects_compensation[0]["winner"][ii] == 1 and settings.projects_compensation[0]["winner"][ii] == settings.projects_compensation[i]["winner"][ii]:
                x += 1
            else:
                pass

        settings.storage_temporary["same_winners"].append(x / sum(settings.projects_compensation[i]["winner"]))


        y = 0
        highest_index_noref = settings.projects_compensation[0]["bid_through"].index(max(settings.projects_compensation[0]["bid_through"]))
        highest_index_current = settings.projects_compensation[i]["bid_through"].index(max(settings.projects_compensation[i]["bid_through"]))
        if highest_index_noref == highest_index_current:
            y = 1
        else:
            pass
        settings.storage_temporary["same_marginal_project"].append(y)


# Stores averages from store data temporary
def store_data():
    storage_temporary_tobeappended = pd.DataFrame.from_dict(settings.storage_temporary, orient='index').transpose()
    storage_temporary_tobeappended = storage_temporary_tobeappended.groupby(["compensation"]).apply(lambda x: x.mean())

    for i in ["pdf", "pdf_parameter1", "pdf_parameter2"]:
        storage_temporary_tobeappended[i] = settings.storage_temporary[i][0]

    global df_storage
    settings.df_storage = settings.df_storage.append(storage_temporary_tobeappended)
    settings.df_storage = settings.df_storage.reset_index(drop=True)


# Just plays the code above for german approach
def do_the_calc_germ():
    gen_projects_germ()
    compensation_calc()
    store_data_temporary()

# Just plays the code above for general approach
def do_the_calc():
    gen_projects()
    compensation_calc()
    store_data_temporary()