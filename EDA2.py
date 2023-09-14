import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging
import pymc3 as pm
import numpy as np
from joblib import Parallel, delayed
import theano.tensor as tt  # Importing theano.tensor to handle PyMC3 math operations

# Import sklearn components conditionally to handle missing modules
try:
    from sklearn.metrics import mean_squared_error
    from sklearn.model_selection import train_test_split
except ImportError as e:
    logging.error(f'Sklearn modules could not be imported: {e}')
    raise

# Initialize logging
logging.basicConfig(filename='data_analysis.log', level=logging.INFO)

try:
    logging.info('Loading data...')
    df = pd.read_csv('your_preprocessed_data.csv')

    logging.info('Starting EDA...')
    
    def plot_data(column):
        plt.figure()
        sns.histplot(df[column])
        plt.title(f'Histogram for {column}')
        plt.savefig(f'{column}_hist.png')

    Parallel(n_jobs=4)(delayed(plot_data)(col) for col in df.columns)

    correlation_matrix = df.corr()
    print(correlation_matrix)
    logging.info('Correlation matrix computed.')

    logging.info('Starting model development...')
    
    selected_features = df.columns.tolist()
    
    X_train, X_test, y_train, y_test = train_test_split(df[selected_features], df['target'], test_size=0.2)

    with pm.Model() as model:  # Using fully qualified name for PyMC3's Model
        alpha = pm.Normal('alpha', mu=0, sigma=1)
        beta = pm.Normal('beta', mu=0, sigma=1, shape=len(selected_features))
        sigma = pm.HalfNormal('sigma', sigma=1)
        
        mu_value = alpha + tt.dot(X_train, beta)  # Avoiding reassignment by using mu_value
        y_obs = pm.Normal('y_obs', mu=mu_value, sigma=sigma, observed=y_train)  # Using mu_value
        
        trace = pm.sample(5000, tune=2000, target_accept=0.9, cores=4)

    logging.info('Model trained.')

    ppc = pm.sample_posterior_predictive(trace, model=model, samples=5000)
    y_pred = ppc['y_obs'].mean(axis=0)
    
    mse = mean_squared_error(y_test, y_pred)
    print('Mean Squared Error:', mse)
    logging.info(f'Mean Squared Error: {mse}')

except Exception as e:
    logging.error(f'An error occurred: {e}')
