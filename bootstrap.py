import sys
import numpy
import sklearn
import random

def bootstrap(data, confidence=0.95, iterations=10000,
              sample_size=1.0, statistic=numpy.mean):
    n_size = int(len(data) * sample_size)

    stats = list()
    for i in range(iterations):
      sample = sklearn.utils.resample(data, n_samples=n_size)
      stat = statistic(sample)
      stats.append(stat)

    ostats = sorted(stats)
    lower = numpy.percentile(ostats, (1 - confidence) / 2)
    upper = numpy.percentile(ostats, confidence + ((1 - confidence) / 2))

    return (str(statistic), lower, upper)

# Generate 1m random numbers
a = 1
b = 1000000
n = 100000
data = random.sample(xrange(a, b), 100000)
print 'Generated %d random data points between %d and %d' % (n, a, b)

# Generate confidence intervals on the mean
confidence = 0.95
iterations = 1000
sample_size = 0.5
name, lower, upper = bootstrap(data, confidence=confidence, iterations=iterations, sample_size=sample_size)
print '%.1f%% CI (%s): %.1f -- %.1f (%d iterations, %.1f%% sample size)' % (confidence * 100, name, lower, upper, iterations, sample_size * 100)
