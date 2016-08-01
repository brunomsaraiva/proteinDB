"""This module contains the classes and functions needed to read a csv table and generate an html table,
containing the queried data"""

import pandas as pd

# search "algorithm" requires exactly the same name and no spaces
# before or after the keywords in db


class DataParser(object):
    """Main class of module.
    Contains methods to read and parse a csv dataset and methods to
    generate an html table"""

    def __init__(self):
        self.dataset = None
        self.unique_pathologies = None
        self.unique_biofluids = None

    def read_from_csv(self):
        self.dataset = pd.read_csv("C:\Coding\ProteinDB\ProteinDB\ProteinDB\static\dataset\dataset.csv", sep=";")
        pd.set_option('display.max_colwidth', -1)
        self.unique_pathologies = list(set(list(self.dataset["Disease/Condition"])))
        self.unique_biofluids = list(set(list(self.dataset["Sample"])))

    def search_protein(self, protein_name):
        filtered_list = self.dataset[self.dataset["Protein"].str.contains(protein_name)]

        table = self.generate_html_table(filtered_list)
        query_link = self.generate_query_link(list(filtered_list["Accession"]))

        return table, query_link

    def search_pathology(self, pathology_name, conc_var):
        if conc_var == "Any":
            filtered_list = self.dataset
        elif conc_var == "higher":
            filtered_list = self.dataset[self.dataset["Change"] == "+"]
        elif conc_var == "lower":
            filtered_list = self.dataset[self.dataset["Change"] == "-"]

        filtered_list = filtered_list[filtered_list["Disease/Condition"] == pathology_name]

        table = self.generate_html_table(filtered_list)
        query_link = self.generate_query_link(list(filtered_list["Accession"]))

        return table, query_link

    def search_biofluid(self, biofluid_name, pathology_name, conc_var):
        if conc_var == "Any":
            filtered_list = self.dataset
        elif conc_var == "higher":
            filtered_list = self.dataset[self.dataset["Change"] == "+"]
        elif conc_var == "lower":
            filtered_list = self.dataset[self.dataset["Change"] == "-"]

        if pathology_name == "Any":
            pass
        else:
            filtered_list = filtered_list[filtered_list["Disease/Condition"] == pathology_name]

        filtered_list = filtered_list[filtered_list["Sample"] == biofluid_name]

        table = self.generate_html_table(filtered_list)
        query_link = self.generate_query_link(list(filtered_list["Accession"]))

        return table, query_link

    def generate_html_table(self, filtered_data):
        table_classes = ["table", "table-responsive", "search-table", "table-hover"]
        return filtered_data.to_html(classes=table_classes, index=False)

    def generate_query_link(self, list_of_ids):
        link = "http://string-db.org/api/image/network?identifiers="

        sep = "&0D"
        link += sep.join(list_of_ids)

        link += "&species=9606&network_flavor=evidence"

        return link
