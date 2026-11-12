from sklearn.linear_model import Lasso, Ridge
from sklearn.datasets import make_regression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

# Generate sample data
X, y = make_regression(
    n_samples=100,
    n_features=10,
    noise=20,
    random_state=42
)

# Lasso
lasso = make_pipeline(
    StandardScaler(),
    Lasso(alpha=10)
)

# Ridge
ridge = make_pipeline(
    StandardScaler(),
    Ridge(alpha=10)
)

lasso.fit(X, y)
ridge.fit(X, y)

print("Lasso coefficients:")
print(lasso.named_steps['lasso'].coef_)

print("\nRidge coefficients:")
print(ridge.named_steps['ridge'].coef_)
