
import re
import string
import pandas as pd
import nltk
from nltk.corpus import stopwords

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

nltk.download("stopwords", quiet=True)
STOPWORDS = set(stopwords.words("english"))

#ingest the dataset into the program
train_ds ='/content/sample_data/email_enrun_train.csv'
test_ds  ='/content/sample_data/email_enrun_test.csv'
valid_ds ='/content/sample_data/email_enrun_valid.csv'

train_df= pd.read_csv(train_ds)
test_df= pd.read_csv(test_ds)
valid_df= pd.read_csv(valid_ds)

DATA_PATH = pd.concat(
    [train_df, test_df, valid_df],
    ignore_index=True
)

DATA_PATH["label"].value_counts() #balanced
# 1-----> spam
# 0-----> ham

# 1. Load the messages and labels
# ---------------------------------------------------------------------
def load_data(path) -> pd.DataFrame:

    """
    Loads the dataset and returns a DataFrame with columns: label, message.
    Handles both the raw UCI TSV format and the common Kaggle CSV format
    (v1/v2 columns, latin-1 encoded).
    """

    try:

        # Kaggle-style CSV: columns v1 (label), v2 (message), extra junk cols
        #df = pd.read_csv(path, encoding="latin-1")

        if {"v1", "v2"}.issubset(path.columns):
            path = path[["v1", "v2"]].rename(columns={"v1": "label", "v2": "message"})
        elif {"label", "message"}.issubset(path.columns):
            path = path[["label", "message"]]
        elif {"label", "text"}.issubset(path.columns):
            path = path[["label", "text"]].rename(columns={"label": "label", "text": "message"})
            path["label"] = path["label"].map({ 0:"ham", 1:"spam"})
        else:
            raise ValueError("Unrecognized column format")

    except Exception:

        # Fall back to raw UCI tab-separated format (no header)
        df = pd.read_csv(path, sep="\t", header=None, names=["label", "message"])

    df = path.dropna(subset=["label", "message"]).drop_duplicates()
    return df

# 2. Preprocess the text
# ---------------------------------------------------------------------

def preprocess_text(text: str) -> str:

    """Lowercase, strip punctuation/numbers,
    remove stopwords, tokenize."""

    text = text.lower()

    # remove numbers/punctuation
    text = re.sub(r"[^a-z\s]", " ", text)

    # simple tokenization
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOPWORDS and len(t) > 1]

    return " ".join(tokens)


def combined_text(df, column_name):
    return " ".join(df[column_name].astype(str))

combined_text = combined_text(DATA_PATH, "text")

print(combined_text)


from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_wordcloud(combined_text):

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color="white",
        max_words=200,
        collocations=False
    ).generate(combined_text)

    plt.figure(figsize=(15, 7))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()


from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
# 3-6. Full pipeline: vectorize, split, train, evaluate
# --------------------------------------------------------------------

def main():

    print("Loading data...")
    df = load_data(DATA_PATH)

    print("Preprocessing text...")
    df["clean_message"] = df["message"].apply(preprocess_text)

    df["label"] = df["label"].str.lower().map({"ham": 0, "spam": 1})

    print()
    print(df.head(3))
    print()

    print("WORLDCLOUD")
    create_wordcloud(" ".join(df["clean_message"]))

    print()

    df = df.dropna(subset=["label"])

    print()

    print(f"Loaded {len(df)} messages "
          f"({(df['label']==1).sum()} spam, {(df['label']==0).sum()} ham)")

    print()

    print("Vectorizing (TF-IDF)...")
    vectorizer = TfidfVectorizer(max_features=3000)

    X = vectorizer.fit_transform(df["clean_message"])
    y = df["label"]

    print("Splitting train/test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    models = {
        "Naive Bayes": MultinomialNB(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
    }

    for name, model in models.items():
        print(f"\n=== {name} ===")
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        print(f"Accuracy : {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall   : {rec:.4f}")
        print(f"F1 score : {f1:.4f}")

        print("\nClassification report:")
        print(classification_report(y_test, y_pred, target_names=["ham", "spam"]))

        print("Confusion matrix:")
        print(confusion_matrix(y_test, y_pred))

        cm = confusion_matrix(y_test, y_pred)

        disp = ConfusionMatrixDisplay(
               confusion_matrix=cm,
               display_labels=["HAM", "SPAM"]
               )

        disp.plot()

        plt.title(f"{name} - Confusion Matrix")
        plt.xlabel("Predicted Label")
        plt.ylabel("Actual Label")
        plt.show()

        # ------------------------------------------------------------
        # Try it on a few custom examples using the last trained model
        # ------------------------------------------------------------

        #print("\n=== Sample predictions (Logistic Regression) ===")
        print(f"\n=== Sample predictions {name}  ===")

        samples = [
                  "IMPORTANT: YOU WON A NEW VEHICLE FROM OUR COMPANY",
                  #"Congratulations! You've won a $1000 gift card. Click here to claim now!",
                  "Hey, are we still meeting for lunch tomorrow?",
                  "URGENT: Your account has been suspended. Verify your details immediately.",
                  ]

        clean_samples = [preprocess_text(s) for s in samples]

        X_samples = vectorizer.transform(clean_samples)

        models["Logistic Regression"].fit(X_train, y_train)
        preds = models["Logistic Regression"].predict(X_samples)
        for text, pred in zip(samples, preds):
            label = "SPAM" if pred == 1 else "HAM"
            print(f"[{label}] {text}")


if __name__ == "__main__":
     main()


























