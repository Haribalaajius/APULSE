import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import json
import warnings
import os
warnings.filterwarnings("ignore")

# Create static folder
os.makedirs("static", exist_ok=True)

# ML MODELS
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_recall_curve

# XGBOOST
from xgboost import XGBClassifier

# DL
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Conv1D, MaxPooling1D, Flatten

# LOAD DATASET
print("\n📌 Loading Dataset...")
df = pd.read_csv("grid_fault_dataset.csv")
X = df[['voltage', 'current', 'frequency']]

le = LabelEncoder()
y = le.fit_transform(df['status'])
joblib.dump(le, "label_encoder.pkl")

# TRAIN-TEST SPLIT
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

joblib.dump(scaler, "scaler.pkl")

# -------------------------
# EXTRA PLOTS
# -------------------------
# CLASS DISTRIBUTION
plt.figure(figsize=(6,4))
sns.countplot(x=df['status'], palette="magma")
plt.title("Fault Class Distribution")
plt.savefig("static/class_distribution.png")
plt.close()

# CORRELATION HEATMAP
plt.figure(figsize=(6,5))
sns.heatmap(df[['voltage','current','frequency']].corr(), annot=True, cmap="coolwarm")
plt.title("Correlation Heatmap")
plt.savefig("static/correlation_heatmap.png")
plt.close()

# -------------------------
# TRAIN ML MODELS
# -------------------------
models = {
    "KNN": KNeighborsClassifier(n_neighbors=5),
    "SVM": SVC(probability=True),
    "RandomForest": RandomForestClassifier(n_estimators=200),
    "XGBoost": XGBClassifier(
        n_estimators=200, max_depth=5,
        learning_rate=0.1, subsample=0.9,
        eval_metric='mlogloss'
    )
}

accuracies = {}
best_model = None
best_score = 0
best_model_name = ""

def save_cm(cm, name):
    plt.figure(figsize=(5,4))
    sns.heatmap(cm, annot=True, cmap="Blues", fmt="d")
    plt.title(name)
    plt.savefig(f"static/cm_{name}.png")
    plt.close()

print("\n⚡ Training ML Models...")

for name, model in models.items():
    print(f"\n🔵 Training {name}...")
    model.fit(X_train_scaled, y_train)
    pred = model.predict(X_test_scaled)

    acc = accuracy_score(y_test, pred)
    accuracies[name] = acc

    print(f"{name} Accuracy → {acc*100:.2f}%")

    cm = confusion_matrix(y_test, pred)
    save_cm(cm, name)

    if acc > best_score:
        best_score = acc
        best_model = model
        best_model_name = name

# -------------------------
# LSTM & CNN
# -------------------------
X_train_dl = X_train_scaled.reshape(-1, 3, 1)
X_test_dl = X_test_scaled.reshape(-1, 3, 1)
num_classes = len(np.unique(y))

# LSTM
print("\n⚡ Training LSTM...")
lstm = Sequential([
    LSTM(64, input_shape=(3,1)),
    Dense(32, activation='relu'),
    Dense(num_classes, activation='softmax')
])
lstm.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
hist_lstm = lstm.fit(X_train_dl, y_train, epochs=20, batch_size=8, validation_data=(X_test_dl,y_test), verbose=0)

lstm_pred = lstm.predict(X_test_dl).argmax(axis=1)
lstm_acc = accuracy_score(y_test, lstm_pred)
accuracies["LSTM"] = lstm_acc
save_cm(confusion_matrix(y_test,lstm_pred), "LSTM")

# CNN
print("\n⚡ Training 1D-CNN...")
cnn = Sequential([
    Conv1D(32, kernel_size=2, activation='relu', input_shape=(3,1)),
    MaxPooling1D(1),
    Flatten(),
    Dense(32, activation='relu'),
    Dense(num_classes, activation='softmax')
])
cnn.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
hist_cnn = cnn.fit(X_train_dl, y_train, epochs=20, batch_size=8, validation_data=(X_test_dl,y_test), verbose=0)

cnn_pred = cnn.predict(X_test_dl).argmax(axis=1)
cnn_acc = accuracy_score(y_test, cnn_pred)
accuracies["1D-CNN"] = cnn_acc
save_cm(confusion_matrix(y_test,cnn_pred),"1D-CNN")

# -------------------------
# ACCURACY COMPARISON PLOT
# -------------------------
plt.figure(figsize=(10,6))
plt.bar(accuracies.keys(),[v*100 for v in accuracies.values()],color="cyan")
plt.title("Model Accuracy Comparison")
plt.savefig("static/accuracy_comparison.png")
plt.close()

# -------------------------
# FEATURE IMPORTANCE
# -------------------------
rf = models["RandomForest"]
plt.figure(figsize=(6,4))
sns.barplot(x=rf.feature_importances_, y=X.columns)
plt.title("Feature Importance - RF")
plt.savefig("static/feature_importance.png")
plt.close()

# -------------------------
# SAVE BEST MODEL + JSON
# -------------------------
if best_model_name in ["LSTM", "1D-CNN"]:
    best_model.save("best_model_dl.h5")
else:
    joblib.dump(best_model, "best_model.pkl")

results_data = {
    "best_model": best_model_name,
    "best_accuracy": float(best_score),
    "all_accuracies": {k: float(v) for k,v in accuracies.items()},
}

with open("model_results.json", "w") as f:
    json.dump(results_data, f, indent=4)

print("\n✅ Training Completed Successfully!")