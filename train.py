import pickle
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


from sklearn.svm import SVC

# read dataset
df = pd.read_csv('./data/youtube-comments-dataset.csv')
df.head()
# change to lowercase
df.columns = df.columns.str.lower()
df.head()
df = df.dropna()

# Encode sentiment labels into numbers
le = LabelEncoder()
df["sentiment"] = le.fit_transform(df["sentiment"])


# separate X and y
# X= "Comment" only
X = df['comment']

# Target (y) = "sentiment" column
y = df["sentiment"]        # y is a Series


X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Convert text data to numerical features using TfidfVectorizer
tfidf = TfidfVectorizer()
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

#  training the model
model = SVC(
    C=10,
    kernel='rbf'
)
model.fit(X_train_tfidf, y_train)
# Training accuracy
train_accuracy = model.score(X_train_tfidf, y_train)

# Predict on test data and compute test accuracy
y_test_pred = model.predict(X_test_tfidf)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Print results
print("Training Accuracy:", train_accuracy)
print("Test Accuracy:", test_accuracy)

# Save the model and vectorizer
with open(r"..\yt-comment_sentiment-analysis\model.bin", "wb") as file_out:
    pickle.dump(model, file_out)

with open(r"..\yt-comment_sentiment-analysis\vectorizer.pkl", "wb") as file_out:
    pickle.dump(tfidf, file_out)
