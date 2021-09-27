import pandas as pd
from dataclasses import dataclass
from enum import Enum, auto
from pandas.core import groupby
import matplotlib.pyplot as plt
import numpy as np
from pandas.io.pytables import GenericDataIndexableCol
import matplotlib


class DataType(Enum):

    DATASET = pd.DataFrame()


@dataclass
class DataAnalysis:

    dataset: DataType.DATASET

    def show_data(self) -> None:
        """
        Show dataset.
        """
        print(self.dataset)

    def __str__(self):
        return (str(self.dataset))

    def annual_flights(self) -> None:
        """
        Determine number of flights each year.
        """

        annual_flights_list = self.dataset["Year"].value_counts().sort_index()
        years = np.arange(1990, 2021)

        print("-"*52)

        for value, year in zip(annual_flights_list, years):
            print(f"Total number of flights in {year} was {value}.")

        print("-"*52)

        plt.plot(np.arange(1990, 2021, 1), annual_flights_list)
        plt.title("Total number of flights each year (1990 - 2020)")
        plt.show()

    def sort_dataset_by_date(self) -> DataType.DATASET:
        """
        Sort dataset so it is in chronological order.
        """

        self.dataset = self.dataset.sort_values("data_dte")

        return self.dataset

    def busiest_airports(self, domestic: bool) -> None:
        """
        Finds which airports had most flights between 1990 - 2020.

        domestic: True returns busiest US airports. 
        domestic: False returns busiest International airports. 

        """

        if domestic:

            print("Busiest domestic airports: ")
            print(self.dataset["usg_apt"].value_counts(
            ).sort_values(ascending=False))

        else:

            print("Busiest international airports: ")
            print(self.dataset["fg_apt"].value_counts(
            ).sort_values(ascending=False))

    def column_frequent_values(self, column: str) -> pd.Series(dtype="object"):
        """
        Determine value frequencies in a particular column of dataset.
        """

        sorted_series = self.dataset[column].value_counts(
        ).sort_values(ascending=False)

        print(sorted_series)

        return sorted_series

    def type_of_flight(self):
        """
        Determine number of Scheduled and Chartered Flights per Year.
        """

        grouped_values = self.dataset.groupby(["Year"]).sum().iloc[:, -3:-1]
        print("Number of Scheduled and Chartered Flights per Year: \n")

        labels = list(grouped_values.index)

        x = np.arange(len(labels))
        width = 0.35

        fig, ax = plt.subplots(figsize=(10, 10))
        rects1 = ax.bar(
            x - width/2, grouped_values["Scheduled"], width, label='Scheduled Flights')
        rects2 = ax.bar(
            x + width/2, grouped_values["Charter"], width, label='Chartered Flights')

        ax.set_ylabel('Number of Flights')
        ax.set_title('Scheduled and Chartered Flights per Year (1990 - 2020)')
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=60)
        ax.get_yaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        ax.legend()

        plt.show()


if __name__ == "__main__":
    data = DataAnalysis(pd.read_csv("International_Report_Departures.csv"))
    data.show_data()

    data.type_of_flight()
