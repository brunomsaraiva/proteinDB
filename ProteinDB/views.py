"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from ProteinDB import app
from dataparser import DataParser

dataparser = DataParser()
dataparser.read_from_csv()


@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home',
        year=datetime.now().year,
        unique_pathologies = dataparser.unique_pathologies,
        unique_biofluids = dataparser.unique_biofluids,
    )

@app.route("/searchprotein")
def query_protein():
    """Renders the results of the query"""

    table, link = dataparser.search_protein(request.args["proteinName"])
    return render_template(
        "query_results.html",
        title="Results",
        year=datetime.now().year,
        results = table,
        string_link = link,
        )

@app.route("/searchpathology")
def query_pathology():
    """Renders the results of the query"""

    table, link = dataparser.search_pathology(request.args["pathologyName"], request.args["concVar"])
    return render_template(
        "query_results.html",
        title="Results",
        year=datetime.now().year,
        results = table,
        string_link = link,
        )

@app.route("/searchbiofluid")
def query_biofluid():
    """Renders the results of the query"""

    table, link = dataparser.search_biofluid(request.args["biofluidName"], request.args["pathology2Name"], request.args["concVar"])
    return render_template(
        "query_results.html",
        title="Results",
        year=datetime.now().year,
        results = table,
        string_link = link,
        )