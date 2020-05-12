import pandas as pd
import numpy as np
import settings
import xlsxwriter
from datetime import date

import matplotlib.pyplot as plt
import seaborn as sns

#exports data into excel
class Exporter(object):
    def __init__(self, function_name):
        self.writer = pd.ExcelWriter('Export_Project_{0}.xlsx'.format(function_name), engine='xlsxwriter')
        self.df_projects = pd.DataFrame()
        self.df_projects_compensation = pd.DataFrame()
        self.df_storage = pd.DataFrame()
        self.df_storage_temp = pd.DataFrame()
        self.df_graph = pd.DataFrame()

    def end_info_log(self):
        logframe = pd.DataFrame({"date": date.today(),
                    "iterrations": settings.iterations.var,
                    }, index=[0]).transpose()

        logframe.to_excel(self.writer, sheet_name="log")

        self.writer.save()
        print("All Done")

    def single_round(self):
        self.df_projects = pd.DataFrame.from_dict(settings.projects, orient='index').transpose()
        self.df_projects_compensation = pd.DataFrame.from_dict(settings.projects_compensation, orient='index').transpose()

        self.df_projects.to_excel(self.writer, sheet_name="Project")
        self.df_projects_compensation.to_excel(self.writer, sheet_name="Project_compensation")

    def all_rounds(self):
        settings.df_storage.to_excel(self.writer, sheet_name="all")

    def all_rounds_temp(self):
        self.df_storage_temp = pd.DataFrame.from_dict(settings.storage_temporary, orient='index').transpose()
        self.df_storage_temp.to_excel(self.writer, sheet_name="all_temp")

    def by_compensation(self):
        df_comp = pd.DataFrame.from_dict(settings.storage_temporary, orient='index').transpose()

        for i in ["el_produced", "paid_min", "paid_max", "subsidy_min", "subsidy_max","auction_bid_min_succ", "auction_bid_max_succ", "auction_bid_max_received", "max_poss_bid"]:
            df_comp[i] = df_comp[i].astype(float)

        for i in ["el_produced", "paid_min", "paid_max", "subsidy_min", "subsidy_max","auction_bid_min_succ", "auction_bid_max_succ", "auction_bid_max_received", "max_poss_bid"]:
            doexcelu = df_comp.pivot_table(values=i, index=["density_min", "density_max", "LCOE_min", "LCOE_max", "pdf", "pdf_parameter1", "pdf_parameter2", "supply", "demand", "dem_sup", "other_factors", "el_prices"], columns=["compensation"])
            doexcelu.to_excel(self.writer, sheet_name="by_{0}".format(i))

    def by_compensation_germany(self):
        for i in ["el_produced", "paid_min", "paid_max", "subsidy_min", "subsidy_max","auction_bid_min_succ", "auction_bid_max_succ", "auction_bid_max_received", "max_poss_bid"]:
            settings.df_storage[i] = settings.df_storage[i].astype(float)

        for i in ["el_produced", "paid_min", "paid_max", "subsidy_min", "subsidy_max","auction_bid_min_succ", "auction_bid_max_succ", "auction_bid_max_received", "max_poss_bid"]:
            doexcelu = settings.df_storage.pivot_table(values=i, index=["density_min", "density_max", "pdf", "pdf_parameter1", "pdf_parameter2", "supply", "demand", "dem_sup", "other_factors", "el_prices"], columns=["compensation"])
            doexcelu.to_excel(self.writer, sheet_name="by_{0}".format(i))

    def howgoodis_RF(self):
        doexcelu = settings.df_storage.pivot_table(values="subsidy_max", index=["density_min", "density_max", "pdf", "pdf_parameter1", "pdf_parameter2", "supply", "demand", "dem_sup", "other_factors", "el_prices"], columns=["compensation"])

        doexcelu['Diff'] = doexcelu.iloc[:, 0] - doexcelu.iloc[:, settings.keofnoref]

        doexcelu = doexcelu.pivot_table(values='Diff', index=["dem_sup", "pdf_parameter2"],
                                        columns=["pdf_parameter1"])

        doexcelu.to_excel(self.writer, sheet_name="RY_impact")

        self.df_graph = doexcelu

    def graph_it(self):

        sns.heatmap(self.df_graph, annot=True)
        """
        sns.clustermap(doexcelu, annot=True)
        """
        plt.show()





