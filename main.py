# importing pandas module
import numpy as np
import pandas as pd
import random
import jinja2


def fill_missing_program(missing_column, dependent_column):
    missing_rows = df[df[missing_column].isnull()]
    for i, r in missing_rows.iterrows():
        df.at[i, missing_column] = r['Total Library Count'] - r[dependent_column]


def coloring(text):
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def color_rule(val):
    return ['background-color: red' if x >= 3 else 'background-color: yellow' for x in val]


if __name__ == '__main__':

    # loading data set
    df = pd.read_csv('D:/daya/3 курс, 2 семестър/ПИИ/courseProject/netflix.csv')
    df.style.highlight_null('lightgreen')

    # deleting empty countries
    empty_country_rows = df[df['Country'].isnull()]
    df = df.drop(df.index[empty_country_rows.index])

    # fill missing total library count as sum from tv shows and movies
    empty_sum_rows = df[df['Total Library Count'].isnull()]
    for index, row in empty_sum_rows.iterrows():
        df.at[index, 'Total Library Count'] = row['TV Shows Count'] + row['Movies Count']

    # fill missing tv shows count
    fill_missing_program('TV Shows Count', 'Movies Count')

    # fill missing movies count
    fill_missing_program('Movies Count', 'TV Shows Count')

    # fill missing basic cost
    empty_basic_cost_rows = df[df['Basic Cost'].isnull()]
    for index, row in empty_basic_cost_rows.iterrows():
        # find median in column basic cost
        median = df["Basic Cost"].median()
        # validate basic median cost according to row data
        if median < row['Standard Cost']:
            df.at[index, 'Basic Cost'] = median
        else:
            # find dependence between standard and premium cost to calculate basic cost
            percentage_dif_st_pr = row['Standard Cost'] / row['Premium Cost'] * 100
            df.at[index, 'Basic Cost'] = row['Standard Cost'] * percentage_dif_st_pr / 100
            print('in else statement for basic ' + repr(index) + ' median ' + repr(median) +
                  ' percentage_st_pr ' + repr(percentage_dif_st_pr))

    # fill missing standard cost
    empty_standard_cost_rows = df[df['Standard Cost'].isnull()]
    for index, row in empty_standard_cost_rows.iterrows():
        # find median in column standard cost
        median = df["Standard Cost"].median()
        if row['Basic Cost'] < median < row['Premium Cost']:
            df.at[index, 'Standard Cost'] = median
        else:
            # find average between basic and premium cost in order to fill standard cost
            average_standard = (row['Basic Cost'] + row['Premium Cost']) / 2
            df.at[index, 'Standard Cost'] = average_standard
            print('in else statement for standard ' + repr(index) + ' median ' + repr(median) +
                  ' average_standard ' + repr(average_standard))

    # fill missing premium cost
    empty_premium_cost_rows = df[df['Premium Cost'].isnull()]
    for index, row in empty_premium_cost_rows.iterrows():
        # find median of column premium cost
        median = df["Premium Cost"].median()
        if row['Standard Cost'] < median:
            df.at[index, 'Premium Cost'] = median
        else:
            # find dependence between basic and standard cost in order to calculate missing premium cost
            percentage_dif_bs_st = row['Basic Cost'] / row['Standard Cost'] * 100
            df.at[index, 'Premium Cost'] = row['Standard Cost'] + row['Standard Cost'] * percentage_dif_bs_st / 100
            print('in else statement for premium ' + repr(index) + ' median ' + repr(median) +
                  ' percentage_bs_st ' + repr(percentage_dif_bs_st))

    df.to_csv('D:/daya/3 курс, 2 семестър/ПИИ/courseProject/netflix_filled.csv')

    df_original = pd.read_csv('D:/daya/3 курс, 2 семестър/ПИИ/courseProject/netflix.csv')

    print(df.to_string())
