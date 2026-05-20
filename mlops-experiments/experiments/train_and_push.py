import os
import shutil

import mlflow
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
from prometheus_client import CollectorRegistry, Gauge, push_to_gateway

# --- Configuration ---
MLFLOW_TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://localhost:5000")
PUSHGATEWAY_URL = os.environ.get("PUSHGATEWAY_URL", "localhost:9091")
EXPERIMENT_NAME = "Iris Classification"
BEST_MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "best_model")

# Hyperparameter grid
PARAM_GRID = [
    {"max_iter": 50},
    {"max_iter": 100},
    {"max_iter": 200},
    {"max_iter": 500},
    {"max_iter": 1000},
]

# --- Setup MLflow ---
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

experiment = mlflow.get_experiment_by_name(EXPERIMENT_NAME)
if experiment is None:
    experiment_id = mlflow.create_experiment(EXPERIMENT_NAME)
    print(f"Created experiment '{EXPERIMENT_NAME}' (ID={experiment_id})")
else:
    experiment_id = experiment.experiment_id
    print(f"Using existing experiment '{EXPERIMENT_NAME}' (ID={experiment_id})")

# --- Load data ---
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Run experiments ---
best_accuracy = -1
best_run_id = None

for params in PARAM_GRID:
    with mlflow.start_run(experiment_id=experiment_id) as run:
        run_id = run.info.run_id
        max_iter = params["max_iter"]

        mlflow.log_param("max_iter", max_iter)
        mlflow.log_param("model_type", "LogisticRegression")

        model = LogisticRegression(max_iter=max_iter, random_state=42)
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)

        acc = accuracy_score(y_test, y_pred)
        loss = log_loss(y_test, y_proba)

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("loss", loss)
        mlflow.sklearn.log_model(model, "model")

        print(f"Run {run_id[:8]}: max_iter={max_iter}, accuracy={acc:.4f}, loss={loss:.4f}")

        # Push metrics to PushGateway
        registry = CollectorRegistry()
        g_acc = Gauge("mlflow_accuracy", "Model accuracy", ["run_id"], registry=registry)
        g_loss = Gauge("mlflow_loss", "Model loss", ["run_id"], registry=registry)
        g_acc.labels(run_id=run_id).set(acc)
        g_loss.labels(run_id=run_id).set(loss)
        try:
            push_to_gateway(PUSHGATEWAY_URL, job="mlflow_experiments", registry=registry)
        except Exception as e:
            print(f"  Warning: could not push to PushGateway: {e}")

        if acc > best_accuracy:
            best_accuracy = acc
            best_run_id = run_id

# --- Copy best model locally ---
print(f"\nBest run: {best_run_id} (accuracy={best_accuracy:.4f})")

os.makedirs(BEST_MODEL_DIR, exist_ok=True)
# Clear old best model
for item in os.listdir(BEST_MODEL_DIR):
    path = os.path.join(BEST_MODEL_DIR, item)
    if os.path.isdir(path):
        shutil.rmtree(path)
    else:
        os.remove(path)

artifact_uri = f"runs:/{best_run_id}/model"
local_path = mlflow.artifacts.download_artifacts(artifact_uri, dst_path=BEST_MODEL_DIR)
print(f"Best model saved to {local_path}")
