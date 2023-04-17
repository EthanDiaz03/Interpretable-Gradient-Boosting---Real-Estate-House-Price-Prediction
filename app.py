#changed some stuff in my command prompt
import optuna
from sklearn.model_selection import cross_val_score
import lightgbm as lgb
import xgboost as xgb
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import shap
import pandas as pd
from sklearn.linear_model import LinearRegression
import streamlit as st
from streamlit_shap import st_shap

# Load the CSV file into a pandas DataFrame
train = pd.read_csv("train.csv")

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

#study = optuna.create_study(direction='minimize')
#study.optimize(objective, n_trials=100)
#print('Best Hyperparameters:', study.best_params)
#print('Best RMSE:', -study.best_value)
best_params = {'num_leaves': 169, 'max_depth': 44, 'learning_rate': 0.0010124339167544556, 'n_estimators': 83, 'min_child_samples': 25, 'reg_alpha': 0.0006338598354043378, 'reg_lambda': 1.0120470962516766e-05}
best_lgbm = lgb.LGBMRegressor(**best_params)
best_lgbm.fit(X, y)
st.title("Real Estate House Price Prediction")

st.subheader("MSSubClass:")
a = st.slider('A number between 20-190', value=85, max_value = 190)
st.write("Building Class:", a)

st.subheader("Lot Frontage")
check = st.checkbox("N/A")
b = st.slider('A number between 21-181 or N/A', min_value=21, max_value=181)
if check:
    st.write("Lot Frontage:", 0)
else:
    st.write("Lot Frontage:", b)

st.subheader("Lot Area")
c = st.slider('A number between 1300-215k', min_value = 1300, max_value = 215000)
st.write("Lot Area: ", c)

st.subheader("Year Built")
d = st.slider('A number between 1872-2010', min_value = 1872, max_value = 2010)
st.write("Year Built: ", d)

st.subheader("Remodel Date")
e = st.slider('A number between 1950-2010', min_value = 1950, max_value = 2010)
st.write("Year Remodeled: ", e)

st.subheader("Masonry Veneer Area")
f = st.slider('A number between 0-1120', min_value = 0, max_value = 1120)
st.write("Masonry Veneer Area in square feet: ", f)

st.subheader("Type 1 Finished square feet")
g = st.slider('A number between 0-5644', min_value = 0, max_value = 5644)
st.write("Type 1 Finished square feet: ", g)

st.subheader("Type 2 Finished square feet")
h = st.slider('A number between 0-1474', min_value = 0, max_value = 1474)
st.write("Type 2 Finished square feet: ", h)

st.subheader("Unfinished square feet of basement area")
i = st.slider('A number between 0-2336', min_value = 0, max_value = 2336)
st.write("Unfinished square feet of basement area: ", i)


j = g+h+i
st.subheader("Total square feet of basement area: "+str(j))

st.subheader("First Floor square feet")
k = st.slider('A number between 334-4692', min_value = 334, max_value = 4692)
st.write("First Floor square feet: ", k)

st.subheader("Second Floor square feet")
l = st.slider('A number between 0-2065', min_value = 0, max_value = 2065)
st.write("Second Floor square feet: ", l)

m = k+l
st.subheader("Above grade (ground) living area square feet: "+str(m))

user_input = pd.DataFrame({
    'MSSubClass': [a],
    'LotFrontage': [b],
    'LotArea': [c],  # You can set default values for the other features
    'YearBuilt': [d],
    'YearRemodAdd': [e],
    'MasVnrArea': [f],
    'BsmtFinSF1': [g],
    'BsmtFinSF2': [h],
    'BsmtUnfSF': [i],
    'TotalBsmtSF': [j],
    '1stFlrSF': [k],
    '2ndFlrSF': [l],
    'GrLivArea': [m]
})

predicted_price = model.predict(user_input)[0]

# Display the predicted sale price to the user
st.write("Predicted Sale Price:", predicted_price)

#X_display,y_display = shap.datasets.adult(display=True)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(np.array(user_input).reshape(1, -1))

# Create summary plot with just the user input
fig_summary, ax_summary = plt.subplots()
shap.summary_plot(shap_values, X, plot_type='bar', show=False)
plt.title('Summary Plot with User Input')
st.pyplot(fig_summary)

# Create bar plot with just the user input
fig_bar, ax_bar = plt.subplots()
shap.plots.beeswarm(shap_values[0], show=False)
plt.title('Bar Plot with User Input')
st.pyplot(fig_bar)

#st_shap(shap.force_plot(explainer.expected_value, shap_values[0,:], X_display.iloc[0,:]), height=200, width=1000)
#st_shap(shap.force_plot(explainer.expected_value, shap_values[:1000,:], X_display.iloc[:1000,:]), height=400, width=1000)
