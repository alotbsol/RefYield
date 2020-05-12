import settings
import export
import itertools


def generate_once():
    exp = export.Exporter(function_name="generate_once")

    settings.do_the_calc()

    exp.single_round()
    exp.all_rounds_temp()
    exp.by_compensation()
    exp.end_info_log()


def generate_once_germ():
    global correction_max
    global correction_min
    global correction_max_bid
    global max_possible_bid
    settings.correction_max = 1.29
    settings.correction_min = 0.79
    settings.correction_max_bid = 1

    settings.max_possible_bid = 62 * settings.correction_max_bid


    exp = export.Exporter(function_name="generate_once_germ")

    settings.do_the_calc_germ()

    exp.single_round()
    exp.all_rounds_temp()
    exp.by_compensation()

    exp.end_info_log()


def generate_xtimes():
    global iterations
    settings.iterations.var = settings.iterations.var

    exp2 = export.Exporter(function_name="generate_xtimes")

    for i in range(0, settings.iterations.var):
        settings.do_the_calc()


    exp2.all_rounds_temp()

    settings.store_data()
    exp2.all_rounds()
    exp2.by_compensation()
    exp2.end_info_log()

def generate_xtimes_germ():
    global correction_max
    global correction_min
    global correction_max_bid
    global max_possible_bid
    settings.correction_max = 1.29
    settings.correction_min = 0.79
    settings.correction_max_bid = 1.29

    settings.max_possible_bid = 60 * settings.correction_max_bid

    global iterations
    settings.iterations.var = settings.iterations.var

    exp2 = export.Exporter(function_name="generate_xtimes_germ")

    for i in range(0, settings.iterations.var):
        settings.do_the_calc_germ()


    exp2.all_rounds_temp()

    settings.store_data()
    exp2.all_rounds()
    exp2.by_compensation()
    exp2.howgoodis_RF()
    exp2.end_info_log()

def generate_specific_combination_germ():
    global correction_max
    global correction_min
    global correction_max_bid
    global max_possible_bid
    settings.correction_max = 1.29
    settings.correction_min = 0.79
    settings.correction_max_bid = 1

    settings.max_possible_bid = 62

    global iterations

    settings.iterations.var = settings.iterations.var

    density_list = [[250, 650]]
    LCOE_base_list = [50]
    projectlist = [100]
    winners_proportions_list = [0.2, 0.4, 0.6, 0.8, 0.9, 1, 1.1, 1.5]
    pdf_list = {"linear": ["", ""]}
    el_price_list = [0, 10, 20]
    other_fact_list = [0, 10, 20, 30]

    """
        "random",
        "beta": parameteralfa=pdf_parameter1.var, parameterbeta=pdf_parameter2.var,
        "gauss"     mean = parameteralfa, sd = parameterbeta
        "linear"
        "beta_lin"
    """

    exp3 = export.Exporter(function_name="generate_specific_combination_germ")
    for viii in density_list:
        global density_min
        global density_max

        settings.density_min.var = viii[0]
        settings.density_max.var = viii[1]

        for vii in LCOE_base_list:
            global LCOE_base

            settings.LCOE_base = vii

            for vi in el_price_list:
                global el_price
                settings.el_price.var = vi

                for v in other_fact_list:
                    global others_change
                    settings.others_change.var = v

                    for iv in projectlist:
                        global no_projects
                        settings.no_projects.var = iv

                        for iii in winners_proportions_list:
                            global winning_projects
                            settings.winning_projects.var = round(iii * iv)

                            for ii in pdf_list:
                                global pdf
                                global pdf_parameter1
                                global pdf_parameter2

                                settings.pdf.picked = str(ii)
                                settings.pdf_parameter1.var = pdf_list[ii][0]
                                settings.pdf_parameter2.var = pdf_list[ii][1]

                                for i in range(0, settings.iterations.var):
                                    settings.do_the_calc_germ()

                                settings.store_data()
                                settings.create_storage_temporary()

    exp3.all_rounds()
    """exp3.by_compensation()"""
    exp3.howgoodis_RF()
    exp3.end_info_log()


def generate_specific_combination():
    global correction_max
    global correction_min
    global correction_max_bid
    global max_possible_bid
    settings.correction_max = 10
    settings.correction_min = 0
    settings.correction_max_bid = 1

    settings.max_possible_bid = 80

    global iterations
    settings.iterations.var = 200

    global LCOE_min
    global LCOE_max
    settings.LCOE_min.var = 40
    settings.LCOE_max.var = 70


    projectlist = [100]
    winners_proportions_list = [0.25, 0.5, 0.75, 0.9, 1, 1.1]
    """[0.25, 0.5, 0.75, 1, 1.25]"""

    combinations_input = [0.5, 1, 2]
    """[0.5, 0.666, 1, 1.666, 2]"""
    combinations_created = []
    for pairs in itertools.product(combinations_input, repeat=2):
        combinations_created.append(pairs)

    print(combinations_created)

    global pdf
    settings.pdf.picked = "beta"

    el_price_list = [0]
    other_fact_list = [0, 20]

    exp5 = export.Exporter(function_name="generate_specific_combination")


    for vi in el_price_list:
        global el_price
        settings.el_price.var = vi

        for v in other_fact_list:
            global others_change
            settings.others_change.var = v

            for iv in projectlist:
                global no_projects
                settings.no_projects.var = iv

                for iii in winners_proportions_list:
                    global winning_projects
                    settings.winning_projects.var = round(iii * iv)

                    for ii in range(0, len(combinations_created)):

                        global pdf_parameter1
                        global pdf_parameter2
                        settings.pdf_parameter1.var = combinations_created[ii][0]
                        settings.pdf_parameter2.var = combinations_created[ii][1]

                        for i in range(0, settings.iterations.var):
                            settings.do_the_calc()

                        settings.store_data()
                        settings.create_storage_temporary()

    exp5.all_rounds()
    """exp5.by_compensation()"""
    exp5.howgoodis_RF()
    exp5.end_info_log()
    exp5.graph_it()




def generate_german_auctions():
    global correction_max
    global correction_min
    global correction_max_bid
    global max_possible_bid
    settings.correction_max = 1.29
    settings.correction_min = 0.79
    settings.correction_max_bid = 1.29
    """settings.correction_max_bid = 1.29"""

    #so that everything is built or not.... 0 max bid applicable
    global ifmax_thenmax
    settings.ifmax_thenmax = 0


    global iterations
    settings.iterations.var = settings.iterations.var

    density_list = [[250, 650]]
    LCOE_base_list = [50]

    #submitted/won/max bid
    projectlist = [[214, 80, 70], [293, 100, 70], [259, 100, 70], [99, 70, 63], [60, 67, 63], [71, 67, 63], [40, 67, 63],
     [50, 70, 62], [29, 65, 62], [24, 65, 62], [19, 50, 62], [20, 68, 62], [69, 50, 62], [53, 90, 62], [19, 30, 62],
     ]
    """
    [[214, 80, 70], [293, 100, 70], [259, 100, 70], [99, 70, 63], [60, 67, 63], [71, 67, 63], [40, 67, 63],
     [50, 70, 62], [29, 65, 62], [24, 65, 62], [19, 50, 62], [20, 68, 62], [69, 50, 62], [53, 90, 62], [19, 30, 62],
     ]
    """
    pdf_list = {"random": [0, 0]}
    el_price_list = [0, 40]
    other_fact_list = [0, 10, 20, 40]

    global LCOE_min
    global LCOE_max
    settings.LCOE_min.var = 0
    settings.LCOE_max.var = 0


    exp4 = export.Exporter(function_name="generate_german_auctions")
    for iii in projectlist:
        global no_projects
        global winning_projects
        settings.no_projects.var = iii[0]
        settings.winning_projects.var = iii[1]
        settings.max_possible_bid = iii[2] * settings.correction_max_bid

        for vii in density_list:
            global density_min
            global density_max

            settings.density_min.var = vii[0]
            settings.density_max.var = vii[1]

            for vi in LCOE_base_list:
                global LCOE_base

                settings.LCOE_base = vi

                for v in el_price_list:
                    global el_price
                    settings.el_price.var = v

                    for iv in other_fact_list:
                        global others_change
                        settings.others_change.var = iv

                        for ii in pdf_list:
                            global pdf
                            global pdf_parameter1
                            global pdf_parameter2

                            settings.pdf.picked = str(ii)
                            settings.pdf_parameter1.var = pdf_list[ii][0]
                            settings.pdf_parameter2.var = pdf_list[ii][1]

                            for i in range(0, settings.iterations.var):
                                settings.do_the_calc_germ()

                            settings.store_data()
                            settings.create_storage_temporary()


    exp4.all_rounds()
    exp4.by_compensation_germany()
    exp4.howgoodis_RF()
    exp4.end_info_log()




