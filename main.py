# importing pandas module
from termcolor import colored
import pandas as pd


def fill_missing_program(missing_column, dependent_column, color):
    missing_rows = df[df[missing_column].isnull()]
    for i, r in missing_rows.iterrows():
        result_sub = r['Total Library Count'] - r[dependent_column]
        df.at[i, missing_column] = result_sub
        print(colored('Filling ' + missing_column + ' in row: ' + repr(i) + ' with value: ' + repr(result_sub), color))


if __name__ == '__main__':

    # loading data set
    df = pd.read_csv('netflix.csv')

    # deleting empty countries
    empty_country_rows = df[df['Country'].isnull()]
    indexes = empty_country_rows.index
    df = df.drop(df.index[indexes])
    print(colored(
        'Deleting rows with indexes ' + ' '.join(str(e) for e in indexes) + ' because of missing countries.', 'red'))

    # fill missing total library count as sum from tv shows and movies
    empty_sum_rows = df[df['Total Library Count'].isnull()]
    for index, row in empty_sum_rows.iterrows():
        result_sum = row['TV Shows Count'] + row['Movies Count']
        df.at[index, 'Total Library Count'] = result_sum
        print(colored('Filling Total Library Count in row: ' + repr(index) + ' with value: '
                      + repr(result_sum), 'yellow'))

    # fill missing tv shows count
    fill_missing_program('TV Shows Count', 'Movies Count', 'blue')

    # fill missing movies count
    fill_missing_program('Movies Count', 'TV Shows Count', 'green')

    # fill missing basic cost
    empty_basic_cost_rows = df[df['Basic Cost'].isnull()]
    for index, row in empty_basic_cost_rows.iterrows():
        # find median in column basic cost
        median = df["Basic Cost"].median()
        # validate basic median cost according to row data
        if median < row['Standard Cost']:
            df.at[index, 'Basic Cost'] = median
            print(colored('Filling basic cost in row ' + repr(index) + ' with median ' + repr(median), 'magenta'))
        else:
            # find dependence between standard and premium cost to calculate basic cost
            percentage_dif_st_pr = row['Standard Cost'] / row['Premium Cost'] * 100
            result_val_basic = row['Standard Cost'] * percentage_dif_st_pr / 100
            df.at[index, 'Basic Cost'] = result_val_basic
            print(colored('Filling basic cost in row ' + repr(index) + ' with percentage dependence '
                          + repr(percentage_dif_st_pr) + ' and value ' + repr(result_val_basic), 'magenta'))

    # fill missing standard cost
    empty_standard_cost_rows = df[df['Standard Cost'].isnull()]
    for index, row in empty_standard_cost_rows.iterrows():
        # find median in column standard cost
        median = df["Standard Cost"].median()
        if row['Basic Cost'] < median < row['Premium Cost']:
            df.at[index, 'Standard Cost'] = median
            print(colored('Filling standard cost in row ' + repr(index) + ' with median ' + repr(median), 'cyan'))
        else:
            # find average between basic and premium cost in order to fill standard cost
            average_standard = (row['Basic Cost'] + row['Premium Cost']) / 2
            df.at[index, 'Standard Cost'] = average_standard
            print(colored('Filling standard cost in row ' + repr(index) + ' with calculated average '
                          + repr(average_standard), 'cyan'))

    # fill missing premium cost
    empty_premium_cost_rows = df[df['Premium Cost'].isnull()]
    for index, row in empty_premium_cost_rows.iterrows():
        # find median of column premium cost
        median = df["Premium Cost"].median()
        if row['Standard Cost'] < median:
            df.at[index, 'Premium Cost'] = median
            print(colored('Filling premium cost in row ' + repr(index) + ' with median ' + repr(median), 'grey'))
        else:
            # find dependence between basic and standard cost in order to calculate missing premium cost
            percentage_dif_bs_st = row['Basic Cost'] / row['Standard Cost'] * 100
            result_val_premium = row['Standard Cost'] + row['Standard Cost'] * percentage_dif_bs_st / 100
            df.at[index, 'Premium Cost'] = result_val_premium
            print(colored('Filling premium cost in row ' + repr(index) + ' with percentage dependence '
                          + repr(percentage_dif_bs_st) + ' and value ' + repr(result_val_premium), 'grey'))

    df.to_csv('netflix_filled.csv')

    df_original = pd.read_csv('netflix.csv')