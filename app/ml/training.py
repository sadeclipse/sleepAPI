import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

CAT_COLS = ["gender", "physical_activity_level", "diet_type"]
NUM_COLS = [
    "age",
    "bmi",
    "caffeine_intake_mg",
    "water_intake_liters",
    "screen_time_hours",
    "daily_steps",
    "calories_burned",
    "resting_heart_rate",
    "daily_sleep_hours",
    "deep_sleep_hours",
]
OUT_CLASSES_NUM = 3


def get_train_test(df, cat_cols, num_cols):
    target_cat = df.iloc[:, -1].values
    target_num = df.iloc[:, -2].values

    if target_cat.dtype == object or target_cat.dtype.name == "category":
        le = LabelEncoder()
        target_cat = le.fit_transform(target_cat)

    target_num = target_num.astype(np.float32)

    features = df.drop(columns=[df.columns[-1], df.columns[-2]])

    X_train, X_test, y_cat_train, y_cat_test, y_num_train, y_num_test = (
        train_test_split(
            features, target_cat, target_num, test_size=0.2, random_state=69
        )
    )

    def to_inputs_dict(X_data):
        d = {}
        for col in num_cols:
            d[col] = X_data[col].values
        for col in cat_cols:
            d[col] = X_data[col].astype(str).values
        return d

    return (
        to_inputs_dict(X_train),
        to_inputs_dict(X_test),
        y_cat_train,
        y_cat_test,
        y_num_train,
        y_num_test,
    )


def build_nn(X_train_dict, cat_cols, num_cols, out_classes_num) -> models.Model:
    all_inputs = {}
    encoded_features = []

    for col in num_cols:
        all_inputs[col] = layers.Input(shape=(1,), name=col, dtype=tf.float32)

        numeric_normalizer = layers.Normalization(axis=None)
        numeric_normalizer.adapt(X_train_dict[col])

        encoded_features.append(numeric_normalizer(all_inputs[col]))

    for col in cat_cols:
        all_inputs[col] = layers.Input(shape=(1,), name=col, dtype=tf.string)

        lookup = layers.StringLookup(output_mode="int")
        lookup.adapt(X_train_dict[col])

        num_tokens = lookup.vocabulary_size()
        encoding = layers.CategoryEncoding(num_tokens=num_tokens, output_mode="one_hot")

        col_encoded = encoding(lookup(all_inputs[col]))
        encoded_features.append(col_encoded)

    all_features = layers.concatenate(encoded_features)

    x = layers.Dense(32, activation="relu")(all_features)
    x = layers.Dense(64, activation="relu")(x)
    x = layers.Dropout(0.2)(x)
    x = layers.Dense(128, activation="relu")(x)
    x = layers.Dropout(0.2)(x)

    classification_out = layers.Dense(
        out_classes_num, activation="softmax", name="classification_out"
    )(x)

    numerical_out = layers.Dense(1, activation="linear", name="numerical_out")(x)

    model = models.Model(inputs=all_inputs, outputs=[classification_out, numerical_out])

    model.compile(
        optimizer="adam",
        loss={
            "classification_out": "sparse_categorical_crossentropy",
            "numerical_out": "mse",
        },
        metrics={"classification_out": "accuracy", "numerical_out": "mae"},
    )
    return model


if __name__ == "__main__":
    df = pd.read_csv("C:/Users/user/Desktop/data/sleepapi/app/data/reSS.csv")

    X_train_dict, X_test_dict, y_cat_train, y_cat_test, y_num_train, y_num_test = (
        get_train_test(df, CAT_COLS, NUM_COLS)
    )

    model = build_nn(X_train_dict, CAT_COLS, NUM_COLS, out_classes_num=OUT_CLASSES_NUM)

    model.fit(
        x=X_train_dict,
        y={"classification_out": y_cat_train, "numerical_out": y_num_train},
        epochs=40,
        batch_size=32,
        validation_data=(
            X_test_dict,
            {"classification_out": y_cat_test, "numerical_out": y_num_test},
        ),
    )

    model.save("model.keras")
    print("Модель успешно сохранена!")
