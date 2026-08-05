import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import *
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models


def load_df(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def get_train_test(df: pd.DataFrame):
    features = df.iloc[:, 0:-2]
    target_cat = df.iloc[:, -1]
    le = LabelEncoder()
    target_cat = le.fit_transform(target_cat).astype("int32")
    target_num = df.iloc[:, -2].astype("float32")
    return train_test_split(
        features,
        target_cat,
        target_num,
        test_size=0.2,
        random_state=69,
    )


def build_nn(input_dim, out_classes_num) -> models.Model:
    inputs = tf.keras.Input(shape=(input_dim,))
    x = layers.Dense(32, activation="relu")(inputs)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dense(128, activation="relu")(x)
    classification_out = layers.Dense(
        out_classes_num, activation="softmax", name="classification_out"
    )(x)
    numerical_out = layers.Dense(1, activation="linear", name="numerical_out")(x)

    model = models.Model(inputs=inputs, outputs=[classification_out, numerical_out])
    model.compile(
        optimizer="adam",
        loss={
            "classification_out": "sparse_categorical_crossemtropy",
            "numerical_out": "mse",
        },
        metrics={"classification_out": "accuracy", "numerical_out": "mae"},
    )
    return model


def train_model(
    model: models.Model,
    train_X,
    test_X,
    train_cat_y,
    test_cat_y,
    train_num_y,
    test_num_y,
    epochs=20,
):
    history = model.fit(
        x=train_X,
        y={"classification_out": train_cat_y, "numerical_out": train_num_y},
        validation_data=(
            test_X,
            {"classification_out": test_cat_y, "numerical_out": test_num_y},
        ),
        epochs=epochs,
        batch_size=32,
    )
    return history


def main():
    df = load_df("C:/Users/user/Desktop/data/sleepapi/app/data/reSS.csv")
    (
        train_X,
        test_X,
        train_cat_y,
        test_cat_y,
        train_num_y,
        test_num_y,
    ) = get_train_test(df)
    inp_shape = train_X.shape
    model = build_nn(input_dim=inp_shape[1], out_classes_num=3)
    history = train_model(
        model,
        train_X,
        test_X,
        train_cat_y,
        test_cat_y,
        train_num_y,
        test_num_y,
    )

    print(history)


if __name__ == "__main__":
    main()
