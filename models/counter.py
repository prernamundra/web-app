from collections import Counter
from models import lognRes

def count(profile):
    try:
        t = []
        for i in range(len(profile)):
            t.append(profile[i][0])
        counter = Counter(t)
        keys = list(counter.keys())
        string = ""
        for x in keys:
            string = string + f"{x}:{counter[x]}"
            if keys[-1] == x:
                break
            string = string + "-"
        return string
    except:
        return lognRes.idError(profile)