from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from data.dataset_loading import get_dataframe

def load_and_train():
    df = get_dataframe("app/data/reWine.csv") 
    features = df.iloc[:,0:-1]
    target = df.iloc[:, -1]
    train_X, test_X, train_y, test_y = train_test_split(features, target, test_size=0.2)
    RF = RandomForestClassifier(n_estimators=400
                                )
    RF.fit(X=train_X, y=train_y)
    return RF
    

def main():
    model = load_and_train()    
    print(model)
    
if __name__ == "__main__":
    main()