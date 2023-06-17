import pandas as pd
import datetime as dt

RAW_DATA_NAME = r"C:\Users\huang\Desktop\project1\QQQ.csv"
ANALYSIS_RESULT_DATA_NAME = r"C:\Users\huang\Desktop\project1\result\QQQ-result-huang.csv"
ANALYSIS_FIXED_RESULT_DATA_NAME = r"C:\Users\huang\Desktop\project1\result\QQQ-result-fixed-cost-huang.csv"
ANALYSIS_FIXED_SELL_RESULT_DATA_NAME = r"C:\Users\huang\Desktop\project1\result\QQQ-result-fixed-cost-sell-huang.csv"

""" DO NOT EDIT (BEGIN) """


def read_data(file_name) -> pd.DataFrame:
    return pd.read_csv(file_name)


def write_data(data: pd.DataFrame, file_name: str = ANALYSIS_RESULT_DATA_NAME) -> None:
    return data.to_csv(file_name, index=False, float_format='%.4f')


def is_monday(day: str) -> bool:
    return dt.datetime.strptime(day, '%Y/%m/%d').strftime('%A') == 'Monday'


# 从年数，回报倍数得到年化收益. e.g. 0.1 -> 10% 年化收益
def annual_return(num_of_year: int, gain: float, inflation: float) -> float:
    return pow(gain - inflation, 1 / num_of_year) - 1.0


""" DO NOT EDIT (END) """


# -- TODO: Part 1 (START)
def calculate_scheduled_investment(data: pd.DataFrame) -> ():
    shares = 10
    positions = [0.0]
    cost = [0.0]
    assets = [0.0]
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        # 实现计算方程，每个周一购买shares，其他日期不购买
        #   如果购买，需要增加position仓位，增加cost花费
        #   如果不购买，append前日仓位和花费
        #   然后总需要根据open_price计算asset, 并且加入assets
        if is_monday(date):
            positions.append(positions[-1] + shares)
            cost.append(cost[-1] + open_price * shares)
        else:
            positions.append(positions[-1])
            cost.append(cost[-1])
        assets.append(open_price * positions[-1])
    return positions, cost, assets


# -- TODO: Part 1 (END)


# -- TODO: Part 2 (START)
Positions, Cost, Assets = calculate_scheduled_investment(read_data(RAW_DATA_NAME))
percentage = []
for i in range(1, len(read_data(RAW_DATA_NAME))):
    if Cost[i] == 0:
        percentage.append(0)
    else:
        percentage.append(Assets[i] / Cost[i])
POSITIONS = pd.DataFrame(Positions)
COST = pd.DataFrame(Cost)
ASSETS = pd.DataFrame(Assets)
PERCENTAGE = pd.DataFrame(percentage)

concat_data = pd.concat([read_data(RAW_DATA_NAME), POSITIONS, COST, ASSETS, PERCENTAGE], axis=1, ignore_index=True)
concat_data.columns = ["OPEN", "HIGH", "LOW", "CLOSE", "Volume", "Dividends", "Stock splits", "CODES", "DATES",
                       "POSITIONS", "COST", "ASSETS", "PERCENTAGE"]
write_data(concat_data, ANALYSIS_RESULT_DATA_NAME)


def export_result(data: pd.DataFrame, inflation: float) -> float:
    # 生成 {first_name}_QQQ-result.csv, 目标是跟QQQ-result-expected.csv 一致
    # 在这里调用 calculate_scheduled_investment, 并且赋值
    # 到asset 和cost.
    # 最后返回十年的年化率
    asset = calculate_scheduled_investment(data)[2]  # replace
    cost = calculate_scheduled_investment(data)[1]  # replace
    return annual_return(10, asset[-1] / cost[-1], inflation)  # 10 years


# -- TODO: Part 2 (END)

# -- TODO: Part 3 (START)
# -- Recommend to copy and write to a new .csv file, so we will not mix Part 3 with Part 1 or 2
def calculate_scheduled_investment_fixed_cost(data: pd.DataFrame) -> ():
    positions2 = [0.0]
    cost2 = [0.0]
    assets2 = [0.0]
    for j in range(1, len(data)):
        open_price = data.iloc[j]['OPEN']
        date = data.iloc[j]['DATES']
        if is_monday(date):
            positions2.append(positions2[-1] + (1000 // open_price))
            cost2.append(cost2[-1] + (1000 // open_price) * open_price)
        else:
            positions2.append(positions2[-1])
            cost2.append(cost2[-1])
        assets2.append(open_price * positions2[-1])
    pass
    return positions2, cost2, assets2


positions_fixed, cost_fixed, assets_fixed = calculate_scheduled_investment_fixed_cost(read_data(RAW_DATA_NAME))
percentage_fixed = []
for i in range(1, len(read_data(RAW_DATA_NAME))):
    if cost_fixed[i] == 0:
        percentage_fixed.append(0)
    else:
        percentage_fixed.append(assets_fixed[i] / cost_fixed[i])
POSITIONS_FIXED = pd.DataFrame(positions_fixed)
COST_FIXED = pd.DataFrame(cost_fixed)
ASSETS_FIXED = pd.DataFrame(assets_fixed)
PERCENTAGE_FIXED = pd.DataFrame(percentage_fixed)

concat_data = pd.concat([read_data(RAW_DATA_NAME), POSITIONS_FIXED, COST_FIXED, ASSETS_FIXED, PERCENTAGE_FIXED], axis=1,
                        ignore_index=True)
concat_data.columns = ["OPEN", "HIGH", "LOW", "CLOSE", "Volume", "Dividends", "Stock splits", "CODES", "DATES",
                       "POSITIONS", "COST", "ASSETS", "PERCENTAGE"]
write_data(concat_data, ANALYSIS_FIXED_RESULT_DATA_NAME)


def get_annual_return_fixed_cost(data: pd.DataFrame, inflation: float) -> float:
    asset = calculate_scheduled_investment_fixed_cost(data)[2]  # replace
    cost = calculate_scheduled_investment_fixed_cost(data)[1]  # replace
    return annual_return(10, asset[-1] / cost[-1], inflation)
    pass


# -- TODO: Part 3 (END)


# -- TODO: Part 4 (START)
def calculate_scheduled_investment_fixed_cost_with_sell(data: pd.DataFrame,
                                                        sell_point: float,
                                                        sell_percentage: float) -> ():
    positions3 = [0.0]
    cost3 = [0.0]
    assets3 = [0.0]
    percentage3 = [0.0]
    min_asset = 30000
    min_days = 5
    days = 0
    for i in range(1, len(data)):
        open_price = data.iloc[i]['OPEN']
        date = data.iloc[i]['DATES']
        if assets3[i - 1] >= min_asset and days >= min_days and assets3[i - 1] > cost3[i - 1] * sell_point:
            sell_share = int(positions3[i - 1] * sell_percentage)
            positions3.append(positions3[i - 1] - sell_share)
            cost3.append(cost3[i - 1] - cost3[i - 1] / positions3[i - 1] * sell_share)
            assets3.append(assets3[i - 1] - assets3[i - 1] / positions3[i - 1] * sell_share)
            days = 0
            if cost3[i] > 0:
                percentage3.append(assets3[i] / cost3[i])
            else:
                percentage3.append(0)
            continue
        else:
            days += 1

        if is_monday(date):
            positions3.append(positions3[-1] + (1000 // open_price))
            cost3.append(cost3[i - 1] + (1000 // open_price) * open_price)
        else:
            positions3.append(positions3[-1])
            cost3.append(cost3[i - 1])
        assets3.append(open_price * positions3[-1])
        if cost3[i] > 0:
            percentage3.append(assets3[i] / cost3[i])
        else:
            percentage3.append(0)
        pass
    return positions3, cost3, assets3, percentage3


positions_sell, cost_sell, assets_sell, percentage_sell = calculate_scheduled_investment_fixed_cost_with_sell(
    read_data(RAW_DATA_NAME),
    2, 0.25)
POSITIONS_SELL = pd.DataFrame(positions_sell)
COST_SELL = pd.DataFrame(cost_sell)
ASSETS_SELL = pd.DataFrame(assets_sell)
PERCENTAGE_SELL = pd.DataFrame(percentage_sell)

concat_data = pd.concat([read_data(RAW_DATA_NAME), POSITIONS_SELL, COST_SELL, ASSETS_SELL, PERCENTAGE_SELL], axis=1,
                        ignore_index=True)
concat_data.columns = ["OPEN", "HIGH", "LOW", "CLOSE", "Volume", "Dividends", "Stock splits", "CODES", "DATES",
                       "POSITIONS", "COST", "ASSETS", "PERCENTAGE"]
write_data(concat_data, ANALYSIS_FIXED_SELL_RESULT_DATA_NAME)


def get_annual_return_fixed_cost_with_sell(data: pd.DataFrame, inflation: float) -> float:
    asset = calculate_scheduled_investment_fixed_cost_with_sell(data, 2, 0.25)[2]  # replace
    cost = calculate_scheduled_investment_fixed_cost_with_sell(data, 2, 0.25)[1]  # replace
    return annual_return(10, asset[-1] / cost[-1], inflation)
    pass


# -- TODO: Part 4 (END)


# -- TODO: Part 5 (Bonus)
def print_all_annual_returns() -> (float, float, float):
    # implement - this can simply call the three investment calculation, where they will write three files.
    print("Investment Return 1: ", round(export_result(read_data(ANALYSIS_RESULT_DATA_NAME), 0), 4) * 100, "%")
    print("Investment Return 2: ",
          round(get_annual_return_fixed_cost(read_data(ANALYSIS_FIXED_RESULT_DATA_NAME), 0), 4) * 100, "%")
    print("Investment Return 3: ",
          round(get_annual_return_fixed_cost_with_sell(read_data(ANALYSIS_FIXED_SELL_RESULT_DATA_NAME), 0), 4) * 100,
          "%")


def print_inflation_adjust_annual_returns() -> (float, float, float):
    print_all_annual_returns()
    # implement - this can simply read from the three files generated.
    return1 = export_result(read_data(ANALYSIS_RESULT_DATA_NAME), 0.03)
    return2 = get_annual_return_fixed_cost(read_data(ANALYSIS_FIXED_RESULT_DATA_NAME), 0.03)
    return3 = get_annual_return_fixed_cost_with_sell(read_data(ANALYSIS_FIXED_SELL_RESULT_DATA_NAME), 0.03)
    print("Adjusted Investment Return 1: ", round(return1, 4) * 100, "%")
    print("Adjusted Investment Return 2: ", round(return2, 4) * 100, "%")
    print("Adjusted Investment Return 3: ", round(return3, 4) * 100, "%")


# -- TODO: Part 5 (END)


if __name__ == '__main__':
    print(calculate_scheduled_investment(read_data()))
    print("Investment Return: ", export_result())
