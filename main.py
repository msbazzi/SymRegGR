import numpy as np
import pandas as pd
from pysr import PySRRegressor

FEATURES = ["Ep", "n", "df", "qp", "tau", "sigma"]

def load_inputs(graft_file, flow_file):
    graft = pd.read_csv(graft_file, delim_whitespace=True)
    flow = pd.read_csv(flow_file, delim_whitespace=True)

    data = pd.concat([graft, flow], axis=1)
    X = data[FEATURES].values
    return data, X

def build_symbolic_model():
    return PySRRegressor(
        niterations=200,
        binary_operators=["+", "-", "*", "/"],
        unary_operators=[
            "exp",
            "log",
            "square(x) = x^2",
            "cube(x) = x^3",
        ],
        model_selection="best",
        loss="loss(x, y) = (x - y)^2",
    )

def train_models(X, y_q, y_m):
    q_model = build_symbolic_model()
    m_model = build_symbolic_model()

    q_model.fit(X, y_q)
    m_model.fit(X, y_m)

    return q_model, m_model

def predict_q_m(q_model, m_model, X):
    q_pred = q_model.predict(X)
    m_pred = m_model.predict(X)
    return q_pred, m_pred