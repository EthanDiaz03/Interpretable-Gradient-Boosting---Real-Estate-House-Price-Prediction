#pip install optuna
#pip install lightgbm
import optuna
from sklearn.model_selection import cross_val_score
import lightgbm as lgb
import xgboost as xgb
import numpy as np
import seaborn as sns
#pip install --upgrade shap
import matplotlib.pyplot as plt
import shap
import pandas as pd
from sklearn.linear_model import LinearRegression

# Load the CSV file into a pandas DataFrame
train = pd.read_csv("/content/drive/MyDrive/CS 301/house-prices-advanced-regression-techniques/train.csv")

# Split the data into X (features) and y (target) 
X = train[["MSSubClass", "LotFrontage", "LotArea", "YearBuilt", "YearRemodAdd", "MasVnrArea", "BsmtFinSF1", "BsmtFinSF2", "BsmtUnfSF", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "GrLivArea"]]

y = train[["SalePrice"]]

model = xgb.XGBRegressor().fit(X, y)

# Create an explainer object using the XGBoost model
explainer = shap.Explainer(model)

# Generate SHAP values for your dataset
shap_values = explainer(X)

def objective(trial):
    params = {
        'num_leaves': trial.suggest_int('num_leaves', 2, 256),
        'max_depth': trial.suggest_int('max_depth', 2, 64),
        'learning_rate': trial.suggest_loguniform('learning_rate', 0.001, 1),
        'n_estimators': trial.suggest_int('n_estimators', 50, 1000),
        'min_child_samples': trial.suggest_int('min_child_samples', 1, 100),
        'reg_alpha': trial.suggest_loguniform('reg_alpha', 1e-9, 10.0),
        'reg_lambda': trial.suggest_loguniform('reg_lambda', 1e-9, 10.0),
        'random_state': 42,
        'objective': 'regression',
        'metric': 'rmse'
    }
    lgbm = lgb.LGBMRegressor(**params)
    return cross_val_score(lgbm, X, y, cv=5, scoring='neg_root_mean_squared_error').mean()

study = optuna.create_study(direction='minimize')
study.optimize(objective, n_trials=100)
print('Best Hyperparameters:', study.best_params)
print('Best RMSE:', -study.best_value)
best_params = study.best_params
best_lgbm = lgb.LGBMRegressor(**best_params)
best_lgbm.fit(X, y)
