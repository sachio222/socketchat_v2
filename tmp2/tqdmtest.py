#usr/bin python3

from tqdm import tqdm

# for i in tqdm(range(10000)):
#     pass
i=0 

with tqdm(total=10000) as t:
    while i < 50:
        i += 1
        t.update()
