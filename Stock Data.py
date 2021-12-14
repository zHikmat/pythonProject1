import os
from urllib.request import urlopen

def download_data(data_name):
    url = 'https://query1.finance.yahoo.com/v7/finance/download/' +data_name+ '?period1=1587042293&period2=1618578293&interval=1d&events=history&includeAdjustedClose=true'
    file_name = data_name + '.csv'

    local_path = os.path.join('fin_data', file_name)

    with urlopen(url) as file, open(local_path, 'wb') as f:
        f.write(file.read())

def get_csv_files(dir_path):
    files_list = os.listdir(dir_path)
    csv_files = []
    proj_folder = os.path.abspath('')
    for file in files_list:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(proj_folder, 'fin_data', file))
    return csv_files

def process_csv(file_name):
    processed_data = []
    with open(file_name, 'r') as f:
        lines = f.readlines()
        header = lines.pop(0)
        processed_data.append(header.strip().split(',') + ['Percentage Change'])
        for line in lines:
            daily_data = line.strip().split(',')
            open_price, close_price = float(daily_data[1]), float(daily_data[4])
            change = round(((close_price - open_price) / open_price) * 100, 2)
            processed_data.append(daily_data + [str(change)])
        return processed_data

def write_csv(file_name, write_data):
    if os.path.exists(file_name):
        os.remove(file_name)
    with open(file_name, 'a') as f:
        for data in write_data:
             print(data)

if __name__ == '__main__':
    data_names = ['MSFT', 'GOOG', 'IBM']
    for data_name in data_names:
        download_data(data_name)
    for csv_file in get_csv_files('./fin_data'):
        write_csv(csv_file, process_csv(csv_file))