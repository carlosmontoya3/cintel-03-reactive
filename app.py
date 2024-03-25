import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import render, reactive
import pandas as pd
import seaborn as sns
from palmerpenguins import load_penguins # This package provides the Palmer Penguins dataset

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = load_penguins()

ui.page_opts(title="Montoya-Penguin Data", fillable=True)

# Add sidebar
with ui.sidebar(open="open"):
    
    ui.h2("Sidebar")
    
    # Dropdown input to choose a column
    ui.input_selectize("selected_attribute", "Select Attribute", ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    # Numeric input for Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count",25)

    # Slider input for Seaborn bins
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 0, 100, 25)

    # Checkbox group input to filter species
    ui.input_checkbox_group("selected_species_list", "Select Species", ["Adelie", "Gentoo", "Chinstrap"], selected=["Adelie","Gentoo", "Chinstrap"], inline=True)

    ui.hr()

    # Hyperlink
    ui.a("GitHub", href="https://github.com/carlosmontoya3/cintel-02-data", target="_blank")

# Main content
with ui.layout_columns():
    with ui.card():
        ui.card_header("Histogram: Species") # Histogram title

        @render_plotly
        def penguins_plot1():
            return px.histogram(
                filtered_data(), x=input.selected_attribute(), nbins=input.plotly_bin_count()
            )

    with ui.card():
        ui.card_header("Seaborn Histogram: Species") # Histogram title

        @render.plot
        def penguins_plot2():
            return sns.histplot(
                data=filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
            )


with ui.layout_columns():
    with ui.card():
        ui.card_header("Scatterplot: Species") # Scatterplot title

        @render_plotly
        def plotly_scatterplot():
            # Create a Plotly scatterplot
            # Call px.scatter() function
            # Pass in six arguments
            return px.scatter(
                data_frame=filtered_data(),
                x="body_mass_g",
                y="bill_depth_mm",
                color="species")

with ui.layout_columns():

    @render.data_frame
    def plot1():
        return render.DataGrid(filtered_data())

    @render.data_frame
    def plot2():
        return render.DataTable(filtered_data())

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    return penguins_df[penguins_df["species"].isin(selected_species)]
