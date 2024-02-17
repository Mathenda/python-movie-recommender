import lenskit.datasets as ds
import pandas as pd
from pip._internal.vcs import git

git clone https://github.com/crash-course-ai/lab4-recommender-systems.git

data = ds.MovieLens('lab4-recommender-systems/')

print("Successfully installed dataset.")
