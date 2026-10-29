
from sklearn.semi_supervised import SelfTrainingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import numpy as np

# Load example dataset
data = load_iris()
X = data.data
y = data.target.copy()

# Hide labels for most training examples
rng = np.random.default_rng(42)
unlabelled_indices = rng.choice(
    len(y), size=100, replace=False
)
y[unlabelled_indices] = -1

# -1 represents an unknown label
model = SelfTrainingClassifier(
    RandomForestClassifier(random_state=42),
    threshold=0.8
)

# Train using labelled and unlabelled data
model.fit(X, y)

print("Training completed!")
print("Predictions:", model.predict(X[:5]))
