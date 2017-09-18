"""
Author: Manohar Vanga
Email: mvanga at mpi-sws dot org
Description: a simple module for bootstrapping confidence intervals.

Copyright 2017 Manohar Vanga

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

import random
import numpy
import sklearn

def bootstrap(dataset, confidence=0.95, iterations=10000,
              sample_size=1.0, statistic=numpy.mean):
    """
    Bootstrap the confidence intervals for a given sample of a population
    and a statistic.

    Args:
        dataset: A list of values, each a sample from an unknown population
        confidence: The confidence value (a float between 0 and 1.0)
        iterations: The number of iterations of resampling to perform
        sample_size: The sample size for each of the resampled (0 to 1.0
                     for 0 to 100% of the original data size)
        statistic: The statistic to use. This must be a function that accepts
                   a list of values and returns a single value.

    Returns:
        Returns the upper and lower values of the confidence interval.
    """
    stats = list()
    n_size = int(len(dataset) * sample_size)

    for _ in range(iterations):
        # Sample (with replacement) from the given dataset
        sample = sklearn.utils.resample(dataset, n_samples=n_size)
        # Calculate user-defined statistic and store it
        stat = statistic(sample)
        stats.append(stat)

    # Sort the array of per-sample statistics and cut off ends
    ostats = sorted(stats)
    lval = numpy.percentile(ostats, ((1 - confidence) / 2) * 100)
    uval = numpy.percentile(ostats, (confidence + ((1 - confidence) / 2)) * 100)

    return (lval, uval)

def test():
    """
    A simple test with randomly generated data
    """
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

if __name__ == '__main__':
    test()
