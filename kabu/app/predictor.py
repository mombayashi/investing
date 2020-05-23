import pandas as pd
#from keras.models import load_model
from tensorflow.keras.models import load_model
from investing.settings import BASE_DIR


def generate_X():
    csv_file = '{}/scrapy/softbank_latest.csv'.format(BASE_DIR)
    train_file = '{}/softbank_10years.csv'.format(BASE_DIR)
    X_train = pd.read_csv(train_file)
    X_train.columns = ['date', 'end', 'begin', 'high', 'low', 'volume', 'ratio']
    X_train = X_train.replace([',', 'M', '%'], ['', '', ''], regex=True)
    X_train.end = X_train.end.astype(float)
    X_train.begin = X_train.begin.astype(float)
    X_train.high = X_train.high.astype(float)
    X_train.low = X_train.low.astype(float)
    X_train = X_train[X_train.volume != '-']
    X_train.volume = X_train.volume.astype(float)
    X_train.ratio = X_train.ratio.astype(float)

    df_30days = pd.read_csv(csv_file)

    # 学習に使用したデータの最大、最小を計算する
    feat_order = ['stock_end', 'stock_begin', 'stock_high', 'stock_low', 'stock_vol', 'stock_ratio']
    feat_train_map = {
        'stock_end':'end', 
        'stock_begin':'begin', 
        'stock_high':'high', 
        'stock_low':'low', 
        'stock_vol':'volume', 
        'stock_ratio':'ratio'
    }
    feat_max, feat_min, feat_range = {}, {}, {}
    for feat in feat_order:
        feat_max[feat] = X_train.loc[:, [feat_train_map[feat]]].max()[0]
        feat_min[feat] = X_train.loc[:, [feat_train_map[feat]]].min()[0]
        feat_range[feat] = feat_max[feat] - feat_min[feat]
    
    # csvファイルには次の順番でデータが格納されている
    #   stock_begin,stock_date,stock_end,stock_high,stock_low,stock_ratio,stock_vol
    #   "4,179.0",2020年04月07日,"4,129.0","4,242.0","4,040.0",2.81%,33.35M
    #
    # 学習モデルは次の順番でデータを期待している
    # end	begin	high	low	volume	ratio

    df_30days = df_30days.replace([',', '%', 'M'], ['', '', ''], regex=True)
    df_30days.stock_end = df_30days.stock_end.astype(float)
    df_30days.stock_begin = df_30days.stock_begin.astype(float)
    df_30days.stock_high = df_30days.stock_high.astype(float)
    df_30days.stock_low = df_30days.stock_low.astype(float)
    df_30days.stock_vol = df_30days.stock_vol.astype(float)
    df_30days.stock_ratio = df_30days.stock_ratio.astype(float)

    df_5days = df_30days.loc[:4]
    df_5days.stock_end = (df_5days.stock_end - feat_min['stock_end']) / feat_range['stock_end']
    df_5days.stock_begin = (df_5days.stock_begin - feat_min['stock_begin']) / feat_range['stock_begin']
    df_5days.stock_high = (df_5days.stock_high - feat_min['stock_high']) / feat_range['stock_high']
    df_5days.stock_low = (df_5days.stock_low - feat_min['stock_low']) / feat_range['stock_low']
    df_5days.stock_vol = (df_5days.stock_vol - feat_min['stock_vol']) / feat_range['stock_vol']
    df_5days.stock_ratio = (df_5days.stock_ratio - feat_min['stock_ratio']) / feat_range['stock_ratio']

    # 順番を整形して過去５日分のデータとする
    df_5days = df_5days[['stock_end', 'stock_begin', 'stock_high', 'stock_low', 'stock_vol', 'stock_ratio']]
    return df_5days.to_numpy().tolist()


def run_predict():
    h5_file = '{}/softbank.h5'.format(BASE_DIR)
    model = load_model(h5_file)
    recent_5_days = generate_X()
    #values = model.predict([[recent_5_days,]])
    values = model.predict([recent_5_days,])

    return values[0]


def predict():
    # モデルを実行して今日の予測値を返す関数を定義する

    predicted = run_predict()

    return predicted



if __name__ == '__main__':
    print(predict())
