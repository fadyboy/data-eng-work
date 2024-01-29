import sys
import pandas as pd

job_date = sys.argv[1]

series = pd.Series([12, 23, 45], name="Age")

print(f"{job_date} job completed successfully")