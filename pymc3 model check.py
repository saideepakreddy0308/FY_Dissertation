import sys
import pymc3 as pm

print("Python Executable:", sys.executable)

def create_model():
    with pm.Model() as model:
        alpha = pm.Normal('alpha', mu=0, sigma=1)
        beta = pm.Normal('beta', mu=0, sigma=1)
        sigma = pm.HalfNormal('sigma', sigma=1)
    print("Model created successfully.")

# Invoke the function to create the model
create_model()
