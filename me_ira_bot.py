from configparser import SafeConfigParser
import os
import sys
import random
import time

import praw

# Bot's tagline for owner contact and GitHub link
SETRESPONSE = """
    

    
--------------    
*I am a bot*

[Give my owner a whack of the spoon](https://www.reddit.com/message/compose?to=christianh10992&subject=&message=)

[Source code](https://github.com/christian10992/me_ira_bot)"""


# Establish reddit instance
config = SafeConfigParser()
config.read('config.ini')
reddit = praw.Reddit(user_agent=config.get('Bot', 'user_agent'),
             client_id=config.get('Bot', 'client_id'),
             client_secret=config.get('Bot', 'client_secret'),
             username=config.get('Bot', 'username'),
             password=config.get('Bot', 'password'))


# If code has not been run, store as empty list
if not os.path.isfile('posts_replied_to.txt'):
    posts_replied_to = []
# Else read the file with the list and remove any empty values
else:
    with open('posts_replied_to.txt', 'r') as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))


# Get the top 3 posts from the subreddit and print their information
subreddit = reddit.subreddit('me_ira')
for submission in subreddit.hot(limit=3):
    try:
        print('Title: ', submission.title)
    except:
        # Submissions in the subreddit often contain characters not supported
        # by Python. If a character would raise an exception, it is substituted
        # with a replacement character instead.
        non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
        print(submission.title.translate(non_bmp_map))
    print('Text: ', submission.selftext)
    print('Media: ', submission.secure_media)
    print('Score: ', submission.score)
    print('---------------------------\n')


    # Check to see if this post has been replied to
    if submission.id not in posts_replied_to:
        comment = random.choice(list(open('me_ira.txt')))
        submission.reply(comment + SETRESPONSE)


        # Store the current id in the list
        posts_replied_to.append(submission.id)


        # Write updated list back to file
        with open('posts_replied_to.txt', 'w') as f:
            for post_id in posts_replied_to:
                f.write(post_id + '\n')

        time.sleep(600) # Try next post 10 minutes after commenting)
        

    else:
        time.sleep(4)  # If post found has already been replied to, try next post in 4 seconds
