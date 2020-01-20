import re
from operator import itemgetter

def emojiCounter(tweets):
    print("YES IN")
    a = {}
    emojiCount = {}
    re.compile(r'RT')
    for i in tweets:
        emoji = re.findall(r'[^\w\d\s\'\;\"\[\^\$\.\|\?\*\+\(\)\{\}\/\:!@#$%^&*()\’…\-\|]',i)
        for i in emoji:
            if i not in emojiCount:
                emojiCount[i] = 1
            else:
                emojiCount[i] += 1
    
    # return emojiCount
    a = sorted(emojiCount.items(), key=itemgetter(1), reverse=True)[:3]
    return a