import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import cvxpy as cvx


# interesting se of cumsum

def calculate_arithmetic_rate_of_return(close):
    """
    Compute returns for each ticker and date in close.
    
    Parameters
    ----------
    close : DataFrame
        Close prices for each ticker and date
    
    Returns
    -------
    arithmnetic_returns : Series
        arithmnetic_returns at the end of the period for each ticker
        
    """
    # TODO: Implement Function
    returns = close / close.shift(1) - 1
    arithmetic_returns = returns.cumsum(axis =0).iloc[returns.shape[0]-1]/returns.shape[0]

    return arithmetic_returns
    


def covariance_matrix(returns):
    """
    Create a function that takes the return series of a set of stocks
    and calculates the covariance matrix.
    
    Parameters
    ----------
    returns : numpy.ndarray
        2D array containing stock return series in each row.
                
    Returns
    -------
    x : np.ndarray
        A numpy ndarray containing the covariance matrix
    """
    
    #covariance matrix of returns
    cov = np.cov(returns)
        
    return cov
    
    
def optimize_twoasset_portfolio(varA, varB, rAB):
    """Create a function that takes in the variance of Stock A, the variance of
    Stock B, and the correlation between Stocks A and B as arguments and returns 
    the vector of optimal weights
    
    Parameters
    ----------
    varA : float
        The variance of Stock A.
        
    varB : float
        The variance of Stock B.    
        
    rAB : float
        The correlation between Stocks A and B.
        
    Returns
    -------
    x : np.ndarray
        A 2-element numpy ndarray containing the weights on Stocks A and B,
        [x_A, x_B], that minimize the portfolio variance.
    
    """
    # TODO: Use cvxpy to determine the weights on the assets in a 2-asset
    # portfolio that minimize portfolio variance.
    
    cov = np.sqrt(varA)*np.sqrt(varB)*rAB
    x = cvx.Variable(2)
    P = np.array([[varA, cov],[cov, varB]])
    objective = cvx.Minimize(cvx.quad_form(x,P))
    constraints = [sum(x)==1]
    problem = cvx.Problem(objective, constraints)
    min_value = problem.solve()
    xA,xB = x.value
    
    return xA, xB, min_value
    
xA,xB,min_value = optimize_twoasset_portfolio(0.1, 0.05, 0.25)
print("Weight on Stock A: {:.6f}".format(xA))
print("Weight on Stock B: {:.6f}".format(xB))
print("Min risk: {:.6f}".format(min_value))

import cvxpy as cvx
import numpy as np

def optimize_portfolio(returns, index_weights, scale=.00001):
    """
    Create a function that takes the return series of a set of stocks, the index weights,
    and scaling factor. The function will minimize a combination of the portfolio variance
    and the distance of its weights from the index weights.  
    The optimization will be constrained to be long only, and the weights should sum to one.
    
    Parameters
    ----------
    returns : numpy.ndarray
        2D array containing stock return series in each row.
        
    index_weights : numpy.ndarray
        1D numpy array containing weights of the index.
        
    scale : float
        The scaling factor applied to the distance between portfolio and index weights
        
    Returns
    -------
    x : np.ndarray
        A numpy ndarray containing the weights of the stocks in the optimized portfolio
    """
    # TODO: Use cvxpy to determine the weights on the assets
    # that minimizes the combination of portfolio variance and distance from index weights
    
    # number of stocks m is number of rows of returns, and also number of index weights
    #m = 
    
    #covariance matrix of returns
    #cov = 
    
    # x variables (to be found with optimization)
    #x = 
    
    #portfolio variance, in quadratic form
    #portfolio_variance = 
    
    # euclidean distance (L2 norm) between portfolio and index weights
    #distance_to_index = 
    
    #objective function
    #objective = 
    
    #constraints
    #constraints = 

    #use cvxpy to solve the objective
    
    #retrieve the weights of the optimized portfolio
    #x_values
    m = returns.shape[0]
    cov = np.cov(returns)
    x = cvx.Variable(m)
    portfolio_variance = cvx.quad_form(x, cov)
    distance_to_index = cvx.norm(x - index_weights)
    objective = cvx.Minimize(portfolio_variance + scale * distance_to_index)
    constraints = [x >= 0, sum(x) == 1]
    cvx.Problem(objective, constraints).solve()
    x_values = x.value
    return x_values
    
"""Test with a 3 simulated stock return series"""
days_per_year = 252
years = 3
total_days = days_per_year * years

return_market = np.random.normal(loc=0.05, scale=0.3, size=days_per_year)
return_1 = np.random.uniform(low=-0.000001, high=.000001, size=days_per_year) + return_market
return_2 = np.random.uniform(low=-0.000001, high=.000001, size=days_per_year) + return_market
return_3 = np.random.uniform(low=-0.000001, high=.000001, size=days_per_year) + return_market
returns = np.array([return_1, return_2, return_3])

"""simulate index weights"""
index_weights = np.array([0.9,0.15,0.05])

"""try out your optimization function"""
x_values = optimize_portfolio(returns, index_weights, scale=.00001)

print(f"The optimized weights are {x_values}, which sum to {sum(x_values):.2f}")
