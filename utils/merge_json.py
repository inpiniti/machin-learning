from datetime import datetime

def merge_json_data(json_data1, json_data2):
    # year와 TRD_DD가 같은 데이터를 찾아서 합칩니다.
    merged_data = []
    for data1 in json_data1:
        for data2 in json_data2:
            # TRD_DD 값을 datetime 형식으로 변환합니다.
            trd_dd = datetime.strptime(data2['TRD_DD'], '%Y/%m')
            if data1['year'] == trd_dd.strftime('%Y.%m'):
                merged_data.append({**data1, **data2})
                break

    return merged_data

def merge_quarterly_data(json_data):
    # year와 TRD_DD가 같은 데이터를 찾아서 합칩니다.
    for i in range(1, len(json_data)):
        target_data = json_data[i]
        prev_data = json_data[i-1] if i > 0 else None

        # prev_data가 없는 경우에는 merged_data에 추가하지 않습니다.
        if prev_data is None:
            continue

        target_data['prevSales'] = prev_data['sales']
        target_data['prevOperatingProfit'] = prev_data['operatingProfit']
        target_data['prevNetIncome'] = prev_data['netIncome']
        target_data['prevOperatingProfitRatio'] = prev_data['operatingProfitRatio']
        target_data['prevNetProfitRatio'] = prev_data['netProfitRatio']

    json_data = add_quarterly_change(json_data)

    return json_data

def add_quarterly_change(json_data):
    # 이전 분기 데이터와의 변화율을 계산하여 추가합니다.
    for i in range(1, len(json_data)):
        target_data = json_data[i]

        # 이전 분기 대비 변화율을 계산합니다.
        target_data['salesChange'] = round((target_data['sales'] - target_data['prevSales']) / target_data['prevSales'] * 100, 2)
        target_data['operatingProfitChange'] = round((target_data['operatingProfit'] - target_data['prevOperatingProfit']) / target_data['prevOperatingProfit'] * 100, 2)
        target_data['netIncomeChange'] = round((target_data['netIncome'] - target_data['prevNetIncome']) / target_data['prevNetIncome'] * 100, 2)
        target_data['operatingProfitRatioChange'] = round(target_data['operatingProfitRatio'] - target_data['prevOperatingProfitRatio'], 2)
        target_data['netProfitRatioChange'] = round(target_data['netProfitRatio'] - target_data['prevNetProfitRatio'], 2)

    return json_data

def add_next_quarter_data(json_data):
    # 다음 분기의 MMEND_CLSPRC 필드를 추가합니다.
    for i in range(len(json_data)-1):
        current_data = json_data[i]
        next_data = json_data[i+1]

        nextData = next_data['MMEND_CLSPRC']
        current_data['nextMmendClsprc'] = nextData

        nextData = int(nextData.replace(',', ''))
        currentData = int(current_data['MMEND_CLSPRC'].replace(',', ''))

        # 다음 분기 대비 변화율을 계산합니다.
        current_data['mmendClsprcChange'] = round((nextData - currentData) / currentData * 100, 2)

    return json_data