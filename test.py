import time
from datetime import datetime

a = time.time()
s, d = datetime.fromtimestamp(a).strftime(
                    '%Y-%m-%d %H').split(' ')
print(s, d)