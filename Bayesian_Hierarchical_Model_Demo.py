import pandas as pd
import pymc3 as pm
import aesara.tensor as at
from sklearn.model_selection import train_test_split
import logging
from sklearn.metrics import mean_squared_error

# Initialize logging
logging.basicConfig(filename='hierarchical_model.log', level=logging.INFO)

try:
    logging.info('Loading data...')
    df = pd.read_csv('etf_data/preprocessed_data.csv')  # assuming columns = ['ETF', 'feature_1', 'feature_2', ..., 'target']
    etf_groups = df['ETF'].unique()
    n_etfs = len(etf_groups)

    # Map ETFs to indices for hierarchical modeling
    df['ETF_idx'] = df['ETF'].map({etf: i for i, etf in enumerate(etf_groups)})

    logging.info('Preparing data...')
    selected_features = [col for col in df.columns if col not in ['ETF', 'target', 'ETF_idx']]
    X_train, X_test, y_train, y_test = train_test_split(df[selected_features], df['target'], test_size=0.2, stratify=df['ETF_idx'])

    etf_idx_train = df.loc[X_train.index, 'ETF_idx']
    etf_idx_test = df.loc[X_test.index, 'ETF_idx']

    logging.info('Building hierarchical model...')
    with pm.Model() as hierarchical_model:
        # Hyperpriors
        mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=1)
        sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=1)
        
        mu_beta = pm.Normal('mu_beta', mu=0, sigma=1)
        sigma_beta = pm.HalfNormal('sigma_beta', sigma=1)
        
        # ETF-level random intercepts
        alpha = pm.Normal('alpha', mu=mu_alpha, sigma=sigma_alpha, shape=n_etfs)
        
        # Fixed slopes for each predictor
        beta = pm.Normal('beta', mu=mu_beta, sigma=sigma_beta, shape=len(selected_features))
        
        # Model error
        sigma = pm.HalfNormal('sigma', sigma=1)
        
        # Expected value
        mu = alpha[etf_idx_train] + at.dot(X_train.values, beta)
        
        # Data likelihood
        y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y_train)

        # Sampling
        trace = pm.sample(500, tune=200, target_accept=0.9, cores=4)
        
        # WAIC for model comparison
        waic = pm.waic(trace, scale='deviance')
        logging.info(f'WAIC: {waic.waic}')

    logging.info('Model trained.')

    # Posterior Predictive Checks
    ppc = pm.sample_posterior_predictive(trace, model=hierarchical_model, samples=500)
    y_pred = ppc['y_obs'].mean(axis=0)
    
    mse = mean_squared_error(y_test, y_pred)
    logging.info(f'Mean Squared Error: {mse}')

except Exception as e:
    logging.error(f'An error occurred: {e}')

""" Explanation: Explanation:
Hyperpriors: Added mu_alpha and sigma_alpha as hyperpriors for the random intercepts. Similarly, mu_beta and sigma_beta are hyperpriors for the fixed slopes. This enables you to explore prior sensitivity by varying these hyperparameters.

ETF-level Random Intercept: The variable alpha is now a vector of random intercepts, one for each ETF group. This establishes the hierarchical structure in the model.

WAIC: I added the calculation of Watanabe-Akaike Information Criterion (WAIC) as a measure for model validation.

Note: This code assumes that you've a column named ETF in your DataFrame to identify different ETF groups. Also, replace 'etf_data/preprocessed_data.csv' with your actual CSV file. """