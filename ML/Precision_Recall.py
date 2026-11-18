from sklearn.metrics import (
    precision_recall_curve,
    roc_curve,
    auc,
    average_precision_score,
    roc_auc_score
)

# Actual values
y_true = y_test

# Predicted probabilities for positive class
y_prob = model.predict_proba(X_test)[:, 1]

# Precision-Recall Curve
precision, recall, thresholds = precision_recall_curve(
    y_true, y_prob
)

pr_auc = auc(recall, precision)
ap_score = average_precision_score(y_true, y_prob)

# ROC Curve
fpr, tpr, thresholds = roc_curve(y_true, y_prob)

roc_auc = roc_auc_score(y_true, y_prob)

print("PR-AUC:", pr_auc)
print("Average Precision:", ap_score)
print("ROC-AUC:", roc_auc)
