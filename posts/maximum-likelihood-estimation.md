---
title: "A Brief Introduction to Maximum Likelihood Estimation"
date: 2026-02-15
tags: statistics, research
description: "Understanding one of the most fundamental concepts in statistical inference"
slug: maximum-likelihood-estimation
---

Maximum likelihood estimation (MLE) is one of those concepts that seems abstract until you work through a few examples. The core idea is surprisingly intuitive: given some observed data, what parameter values make that data most likely to have occurred?

## The Basic Principle

Suppose we observe data $x_1, x_2, \ldots, x_n$ from some distribution with parameter $\theta$. The likelihood function is:

$$
L(\theta | x_1, \ldots, x_n) = \prod_{i=1}^{n} f(x_i | \theta)
$$

The MLE $\hat{\theta}$ is the value that maximizes this likelihood. In practice, we usually maximize the log-likelihood instead:

$$
\ell(\theta) = \sum_{i=1}^{n} \log f(x_i | \theta)
$$

## A Simple Example

Let's say we observe $n$ coin flips: some heads, some tails. If $p$ is the probability of heads, then for $k$ heads in $n$ flips:

$$
L(p | k, n) = \binom{n}{k} p^k (1-p)^{n-k}
$$

Taking the derivative and setting it to zero gives us the intuitive answer: $\hat{p} = k/n$.

## Implementation

Here's a simple Python example for estimating the mean of a normal distribution:

```python
import numpy as np
from scipy.optimize import minimize

# Generate some data
true_mean = 5.0
data = np.random.normal(true_mean, 1.0, 100)

# Negative log-likelihood for normal distribution
def neg_log_likelihood(mu):
    return -np.sum(np.log(1/np.sqrt(2*np.pi) * np.exp(-0.5*(data - mu)**2)))

# Find MLE
result = minimize(neg_log_likelihood, x0=0.0)
print(f"MLE estimate: {result.x[0]:.3f}")
print(f"Sample mean: {np.mean(data):.3f}")
```

For this simple case, the MLE and sample mean coincide. But the framework generalizes to much more complex situations.

## Why MLE Matters

MLEs have nice asymptotic properties:
- **Consistency**: $\hat{\theta} \xrightarrow{p} \theta$ as $n \to \infty$
- **Asymptotic normality**: $\sqrt{n}(\hat{\theta} - \theta) \xrightarrow{d} N(0, I(\theta)^{-1})$
- **Efficiency**: Under regularity conditions, the MLE achieves the Cramér-Rao lower bound

These properties make MLE a default choice in many statistical applications, from linear regression to deep learning.
