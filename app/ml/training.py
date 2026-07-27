from sklearn.model_selection import train_test_split

from data.dataset_loading import get_dataframe

def get_features_and_target():
    df = get_dataframe("app/data/reWine.csv") 
    features = df.iloc[:,1:]
    target = df.iloc[:, 0]
    train_X, test_X, train_y, test_y = train_test_split(features, target, test_size=0.2)

def main():
    get_features_and_target()

    
if __name__ == "__main__":
    main()