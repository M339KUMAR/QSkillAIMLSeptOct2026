# ============================================================
# IRIS FLOWER CLASSIFICATION
# ============================================================

# ------------------------------------------------------------
# 1. IMPORT LIBRARIES
# ------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)


# ------------------------------------------------------------
# 2. LOAD THE IRIS DATASET
# ------------------------------------------------------------

iris = load_iris()

# Convert dataset into a Pandas DataFrame
df = pd.DataFrame(
    iris.data,
    columns=iris.feature_names
)

# Add target column
df["target"] = iris.target

# Add species name
df["species"] = df["target"].map(
    {
        0: "setosa",
        1: "versicolor",
        2: "virginica"
    }
)

print("\n================ DATASET =================")
print(df.head())

print("\n================ DATASET SHAPE =================")
print(df.shape)

print("\n================ DATASET INFORMATION =================")
print(df.info())

print("\n================ STATISTICAL SUMMARY =================")
print(df.describe())

print("\n================ CLASS DISTRIBUTION =================")
print(df["species"].value_counts())


# ------------------------------------------------------------
# 3. CHECK FOR MISSING VALUES
# ------------------------------------------------------------

print("\n================ MISSING VALUES =================")
print(df.isnull().sum())


# ------------------------------------------------------------
# 4. VISUAL EXPLORATION
# ------------------------------------------------------------

# ------------------------------------------------------------
# 4A. Scatter Plot
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=df,
    x="sepal length (cm)",
    y="sepal width (cm)",
    hue="species",
    style="species",
    s=100
)

plt.title("Sepal Length vs Sepal Width")
plt.xlabel("Sepal Length (cm)")
plt.ylabel("Sepal Width (cm)")
plt.show()


# ------------------------------------------------------------
# 4B. Petal Length vs Petal Width
# ------------------------------------------------------------

plt.figure(figsize=(8, 6))

sns.scatterplot(
    data=df,
    x="petal length (cm)",
    y="petal width (cm)",
    hue="species",
    style="species",
    s=100
)

plt.title("Petal Length vs Petal Width")
plt.xlabel("Petal Length (cm)")
plt.ylabel("Petal Width (cm)")
plt.show()


# ------------------------------------------------------------
# 4C. Pair Plot
# ------------------------------------------------------------

sns.pairplot(
    df,
    hue="species"
)

plt.show()


# ------------------------------------------------------------
# 4D. Histograms
# ------------------------------------------------------------

df[iris.feature_names].hist(
    figsize=(12, 8),
    bins=15
)

plt.suptitle("Distribution of Iris Features")
plt.show()


# ------------------------------------------------------------
# 5. DEFINE FEATURES AND TARGET
# ------------------------------------------------------------

# X = input features
# y = target/output

X = df[iris.feature_names]

y = df["target"]

print("\n================ FEATURES =================")
print(X.head())

print("\n================ TARGET =================")
print(y.head())


# ------------------------------------------------------------
# 6. TRAIN-TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\n================ TRAIN TEST SPLIT =================")

print("Training samples:", X_train.shape[0])
print("Testing samples :", X_test.shape[0])


# ------------------------------------------------------------
# 7. FEATURE SCALING
# ------------------------------------------------------------

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)

X_test_scaled = scaler.transform(X_test)


# ------------------------------------------------------------
# 8. LOGISTIC REGRESSION
# ------------------------------------------------------------

logistic_model = LogisticRegression(
    max_iter=200
)

logistic_model.fit(
    X_train_scaled,
    y_train
)

logistic_predictions = logistic_model.predict(
    X_test_scaled
)


# ------------------------------------------------------------
# 9. K-NEAREST NEIGHBORS
# ------------------------------------------------------------

knn_model = KNeighborsClassifier(
    n_neighbors=5
)

knn_model.fit(
    X_train_scaled,
    y_train
)

knn_predictions = knn_model.predict(
    X_test_scaled
)


# ------------------------------------------------------------
# 10. DECISION TREE
# ------------------------------------------------------------

decision_tree_model = DecisionTreeClassifier(
    random_state=42
)

decision_tree_model.fit(
    X_train,
    y_train
)

decision_tree_predictions = decision_tree_model.predict(
    X_test
)


# ------------------------------------------------------------
# 11. MODEL EVALUATION FUNCTION
# ------------------------------------------------------------

def evaluate_model(model_name, y_true, y_pred):

    accuracy = accuracy_score(
        y_true,
        y_pred
    )

    precision = precision_score(
        y_true,
        y_pred,
        average="weighted"
    )

    recall = recall_score(
        y_true,
        y_pred,
        average="weighted"
    )

    f1 = f1_score(
        y_true,
        y_pred,
        average="weighted"
    )

    print("\n========================================")
    print(model_name)
    print("========================================")

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    print("\nClassification Report:")
    print(
        classification_report(
            y_true,
            y_pred,
            target_names=iris.target_names
        )
    )

    return accuracy, precision, recall, f1


# ------------------------------------------------------------
# 12. EVALUATE ALL MODELS
# ------------------------------------------------------------

lr_results = evaluate_model(
    "Logistic Regression",
    y_test,
    logistic_predictions
)

knn_results = evaluate_model(
    "K-Nearest Neighbors",
    y_test,
    knn_predictions
)

dt_results = evaluate_model(
    "Decision Tree",
    y_test,
    decision_tree_predictions
)


# ------------------------------------------------------------
# 13. COMPARE MODELS
# ------------------------------------------------------------

results = pd.DataFrame(
    {
        "Model": [
            "Logistic Regression",
            "KNN",
            "Decision Tree"
        ],

        "Accuracy": [
            lr_results[0],
            knn_results[0],
            dt_results[0]
        ],

        "Precision": [
            lr_results[1],
            knn_results[1],
            dt_results[1]
        ],

        "Recall": [
            lr_results[2],
            knn_results[2],
            dt_results[2]
        ],

        "F1 Score": [
            lr_results[3],
            knn_results[3],
            dt_results[3]
        ]
    }
)

print("\n================ MODEL COMPARISON =================")
print(results)


# ------------------------------------------------------------
# 14. VISUALIZE MODEL COMPARISON
# ------------------------------------------------------------

results.set_index("Model").plot(
    kind="bar",
    figsize=(10, 6)
)

plt.title("Model Performance Comparison")
plt.ylabel("Score")
plt.ylim(0, 1.1)
plt.xticks(rotation=0)
plt.legend(loc="lower right")
plt.show()


# ------------------------------------------------------------
# 15. CONFUSION MATRIX - LOGISTIC REGRESSION
# ------------------------------------------------------------

cm_lr = confusion_matrix(
    y_test,
    logistic_predictions
)

plt.figure(figsize=(6, 5))

sns.heatmap(
    cm_lr,
    annot=True,
    fmt="d",
    cmap="Blues",
    xticklabels=iris.target_names,
    yticklabels=iris.target_names
)

plt.title("Confusion Matrix - Logistic Regression")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ------------------------------------------------------------
# 16. CONFUSION MATRIX - KNN
# ------------------------------------------------------------

cm_knn = confusion_matrix(
    y_test,
    knn_predictions
)

plt.figure(figsize=(6, 5))

sns.heatmap(
    cm_knn,
    annot=True,
    fmt="d",
    cmap="Greens",
    xticklabels=iris.target_names,
    yticklabels=iris.target_names
)

plt.title("Confusion Matrix - KNN")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ------------------------------------------------------------
# 17. CONFUSION MATRIX - DECISION TREE
# ------------------------------------------------------------

cm_dt = confusion_matrix(
    y_test,
    decision_tree_predictions
)

plt.figure(figsize=(6, 5))

sns.heatmap(
    cm_dt,
    annot=True,
    fmt="d",
    cmap="Oranges",
    xticklabels=iris.target_names,
    yticklabels=iris.target_names
)

plt.title("Confusion Matrix - Decision Tree")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()


# ------------------------------------------------------------
# 18. PREDICT A NEW IRIS FLOWER
# ------------------------------------------------------------

# Example:
# Sepal Length = 5.1 cm
# Sepal Width  = 3.5 cm
# Petal Length = 1.4 cm
# Petal Width  = 0.2 cm

new_flower = [[
    5.1,
    3.5,
    1.4,
    0.2
]]


# Scale the new data
new_flower_scaled = scaler.transform(
    new_flower
)


# Predict using Logistic Regression
prediction = logistic_model.predict(
    new_flower_scaled
)


predicted_species = iris.target_names[
    prediction[0]
]

print("\n========================================")
print("NEW FLOWER PREDICTION")
print("========================================")

print("Input measurements:", new_flower)

print("Predicted species:", predicted_species)


# ------------------------------------------------------------
# 19. PREDICTION PROBABILITY
# ------------------------------------------------------------

probabilities = logistic_model.predict_proba(
    new_flower_scaled
)

print("\nPrediction probabilities:")

for species, probability in zip(
    iris.target_names,
    probabilities[0]
):

    print(
        species,
        ":", 
        round(probability * 100, 2),
        "%"
    )
