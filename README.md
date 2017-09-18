# Bootstrap Confidence Intervals

This module provides a simple function for bootstrap confidence
intervals on a list of data sampled from an unknown population.

## Installation

The package is available on PyPI and can be installed using `pip`.

    $ pip install pybootstrap

As a general recommendation I suggest using `virtualenv` to keep your main
Python environment clean from auxiliary packages.

# Usage
The main function provided is the `bootstrap` function to be invoked as shown below:

```python
import pybootstrap as pb

pb.bootstrap(dataset, confidence=0.95, iterations=10000, sample_size=1.0, statistic=numpy.mean)
```

- `dataset`    : a list of values, each a sample from an unknown population
- `confidence` : the confidence value (a float between 0 and 1.0). Default is 0.95.
- `iterations` : the number of iterations of resampling to perform. Default is 10000.
- `sample_size`: the sample size for each of the resampled (a float between 0
  `             and 1.0 for 0 to 100% of the original data size).  Default is 1.0.
- `statistic`  : the statistic to use. This must be a function that accepts
               a list of values and returns a single value. Default is numpy.mean.

The function returns the upper and lower values of the confidence interval for the given dataset.

For a quick test, you can use:

```python
import pybootstrap as pb
pb.test()
```

The example function that is executed is shown below:

```python
def generate_random(n_values, min_value, max_value):
    """
    Generate an array of random values for testing.

    Args:
        n_values: The number of random values to generate
        min_value: Define the lower bound of the range to use
        max_value: Define the upper bound of the range to use

    Returns:
        A list containing 'n_values' random values in the range
        between 'min_value' and 'max_value'
    """
    return random.sample(xrange(min_value, max_value), n_values)

# Generate some random data
data = generate_random(1000, 1, 10000)
# Generate confidence intervals on the mean
confidence = 0.95
iterations = 1000
sample_size = 1.0
statistic = numpy.mean
lower, upper = bootstrap(data,
                         confidence=confidence,
                         iterations=iterations,
                         sample_size=sample_size,
                         statistic=statistic)
print('Performed %d iterations (each with %.1f%% original sample length)' %
      (iterations, sample_size * 100))
print('%.1f%% confidence interval (%s):' %
      (confidence * 100, statistic.__name__))

print 'lower: %.1f' % lower
print 'upper: %.1f' % upper
print 'observed: %.1f' % numpy.mean(data)
```
