from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import update_session_auth_hash, login, authenticate
from django.contrib import messages
from django.shortcuts import render, redirect, render_to_response
from nltk.tokenize import sent_tokenize,word_tokenize

from social_django.models import UserSocialAuth

import tweepy
from emojiCounter import emojiCounter
from movieSummary import movieSummaryMaker
from positiveNegativeCounter import posNegCounter
from hatelike import hateLikeMaker
from summary import summaryMaker
from classification import classification, getextra
import urllib.request 

SOCIAL_AUTH_TWITTER_KEY = 'aYZnMPL2vfxJnwJuvWUrmsP4r'
SOCIAL_AUTH_TWITTER_SECRET = 'f6RYr7mKt3KBfG5R2FTbXwooq2AULsFhzwKSJm9v4CgVs8NutQ'

def get_tweets(name, oauthtoken, oauthsecret):
    auth = tweepy.OAuthHandler(SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET)
    auth.set_access_token(oauthtoken, oauthsecret)
    api = tweepy.API(auth)

    alltweets = []
    tweetObject = []
    newTweet = api.user_timeline(screen_name = name, count = 200, include_rts = False)
    tweetObject.extend(newTweet)
    oldestId = tweetObject[-1].id - 1
    for s in newTweet:
        alltweets.append(s.text)
    
   
    while len(newTweet) > 0:
        newTweet = api.user_timeline(screen_name = name,count=200,max_id=oldestId)
        tweetObject.extend(newTweet)
        oldestId = tweetObject[-1].id
        for s in newTweet:
            alltweets.append(s.text)

    return alltweets
   
def reciprocate(maxPersonality):
    if maxPersonality == 'anger':
        return ["You seem to have ANGER ISSUES:", "1. Think before you speak.", " 2. Once you're calm, express your anger.", "3. Get some exercise. ", "4. Take a timeout.", "5. Identify possible solutions.", "6. Stick with 'I' statements.","7. Don't hold a grudge.","8. Use humor to release tension."]
    elif maxPersonality == 'fear':
        return ["You seem to be FEARFUL:", "1. If your fear is commitment, imagine yourself happily with a partner.", "2. If your fear is heights, imagine yourself conquering a tough hike. Connect with the feeling of accomplishment.", "3. If your fear is spiders, imagine yourself seeing a spider and feeling neutral."]
    elif maxPersonality == 'sadness':
        return ["You seem to be SAD:", "1. Talk to someone","2. Meditate","3. Get out in nature.", "4. Give yourself time and permission.", "5. Remember, it will get better","6. Go outside", "7. Work"]
    elif maxPersonality == 'hate':
        return ["You seem to be HATEFUL:" , "1. Distract yourself if you start dwelling on the person you hate", "2. Breathe slowly and deeply when you feel angry.", "3. Write a letter to express your feelings, but don’t send it to them"]
    elif maxPersonality == 'worry':
        return ["You seem to WORRY way too much", "1. Clear clutter", "2. Learn to focus and calm your thoughts", "3. Listen to Music"]
    elif maxPersonality == 'happiness':
        return ["Great! You seem to be HAPPY all the time", "1. Happiness radiates like the fragrance from a flower and draws all good things towards you.", "2. Happiness is not something you postpone for the future; it is something you design for the present.", "3. The best way to pay for a lovely moment is to enjoy it."]
    elif maxPersonality == 'love':
        return ["Great! You seem to be filled with lots of LOVE:", "1. There is only one happiness in this life, to love and be loved.", "2. Love yourself.", "3. Being deeply loved by someone gives you strength, while loving someone deeply gives you courage.", "4. Love is when the other person's happiness is more important than your own."]
    elif maxPersonality == 'surprise':
        return ["Your SURPRISE factor seems to be high!:", "1. Never tell people how to do things. Tell them what to do and they will surprise you with their ingenuity.", "2. To be prepared against surprise is to be trained. To be prepared for surprise is to be educated."]

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password1')
            )
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def getUsername(request):
    message = request.POST.get('message')
    auth = tweepy.OAuthHandler(SOCIAL_AUTH_TWITTER_KEY, SOCIAL_AUTH_TWITTER_SECRET)
    auth.set_access_token('985959117029298176-dJwttpUf5VRojBNHmTiJ0KSyhybgDZS', 'eQfmRap77vQEYrZGbn4XS7lXBwBP42NTnZf9geB4w9N21')

    api = tweepy.API(auth)
    tweets = api.user_timeline(screen_name= message, count=200) 
    abc = [tweet.text for tweet in tweets]
    
    badwords = 0
    # print(request.user.username)

    # ALL PROCESSING here
    #EMOJI COUNT
    emojis = emojiCounter(abc)

    #MOVIE SUMMARY
    MovieSummary = movieSummaryMaker(abc)

    #POSITIVE NEGATIVE TWEETS COUNT
    pos, neg, positiveTweets, negativeTweets = posNegCounter(abc)
    pos=int(pos);
    neg=int(neg);
    #HATE LIKe
    likes, dislikes = hateLikeMaker(abc)

    #SUMMARY BASED ON TWE
    summary, badWordsCount, percent, maximum = summaryMaker(abc,badwords)
    summary += MovieSummary
    #MODEL
    anger,fear,happiness,hate,love,sad,surprise,worry,opennesspositive,opennessnegative,extrovertpositive,extrovertnegative,neuroticpositive,neuroticnegative,aggreablepositive,aggreablenegative,conscientiousnesspositive,conscientiousnessnegative = classification(abc)
    personalityValues = {'anger':anger, 'fear' : fear, 'happiness' : happiness, 'hate' : hate, 'love' : love, 'sad' : sad, 'surprise' : surprise, 'worry' : worry}
    maxOfAll = max(personalityValues, key = personalityValues.get)
    steps = reciprocate(maxOfAll)
    # #EXTRA DATA
    achievement,alcohol,clothing,cooking,family,government,music,party,programming,science = getextra(abc)
    if badWordsCount > 10:
        badWordsSummary = ["1. Enlist the help of a friend.", "2. Identify your triggers and learn to avoid them.", "3. Use a swear jar.", "4. Ping your wrist with a rubber band.", "5. Pretend your grandmother is always within earshot.","6. Avoid explicit music and other swear-happy media.", "7. Convince yourself that swearing is a negative thing", "8. Practice positive thinking.", "9. Be patient with yourself.", "10. Pay attention to your swearing habits."]
    else:
        badWordsSummary = ["You have a pretty good record!"]
    
    return render(request, 'core/mytest.html', {'badWordsSummary' : badWordsSummary, 'steps' : steps, 'achievement':achievement,'alcohol':alcohol,'clothing':clothing,'cooking':cooking,'family':family,'government':government,'music':music,'party':party,'programming':programming,'science':science,'opennesspositive':opennesspositive,'opennessnegative':opennessnegative,'extrovertpositive':extrovertpositive,'extrovertnegative':extrovertnegative,'neuroticpositive':neuroticpositive,'neuroticnegative':neuroticnegative,'aggreablepositive':aggreablepositive,'aggreablenegative':aggreablenegative,'conscientiousnesspositive':conscientiousnesspositive,'conscientiousnessnegative':conscientiousnessnegative,'anger':anger,'fear':fear,'happiness':happiness,'hate':hate,'love':love,'sad':sad,'surprise':surprise,'worry':worry, 'tweets' : tweets , 'emoji' : emojis, 'MovieSummary' : MovieSummary, 'pos' : pos, 'neg' : neg, 'positiveTweets' : positiveTweets, 'negativeTweets' : negativeTweets , 'likes' : likes, 'dislikes' : dislikes, 'summary' : summary, 'badWordsCount' : badWordsCount, 'percent' : percent, 'maximum' : maximum })




# MAIN PAG
@login_required
def home(request):
    instance = UserSocialAuth.objects.filter(user=request.user).get()
    tweets = get_tweets(request.user.username, (instance.tokens).get('oauth_token'), (instance.tokens).get('oauth_token_secret'))
    badwords = 0
    # print(request.user.username)

    # ALL PROCESSING HERE!
    #EMOJI COUNT
    emojis = emojiCounter(tweets)

    #MOVIE SUMMARY
    MovieSummary = movieSummaryMaker(tweets)

    #POSITIVE NEGATIVE TWEETS COUNT
    pos, neg, positiveTweets, negativeTweets = posNegCounter(tweets)
    pos = int(pos)
    neg = int(neg)
    #HATE LIKE 
    likes, dislikes = hateLikeMaker(tweets)

    #SUMMARY BASED ON TWEET
    summary, badWordsCount, percent, maximum = summaryMaker(tweets,badwords)
    summary += MovieSummary
    #MODEL
    anger,fear,happiness,hate,love,sad,surprise,worry,opennesspositive,opennessnegative,extrovertpositive,extrovertnegative,neuroticpositive,neuroticnegative,aggreablepositive,aggreablenegative,conscientiousnesspositive,conscientiousnessnegative = classification(tweets)
    personalityValues = {'anger':anger, 'fear' : fear, 'happiness' : happiness, 'hate' : hate, 'love' : love, 'sad' : sad, 'surprise' : surprise, 'worry' : worry}
    maxOfAll = max(personalityValues, key = personalityValues.get)
    steps = reciprocate(maxOfAll)
    # #EXTRA DATA
    achievement,alcohol,clothing,cooking,family,government,music,party,programming,science = getextra(tweets)
    if badWordsCount > 10:
        badWordsSummary = ["1. Enlist the help of a friend.", "2. Identify your triggers and learn to avoid them.", "3. Use a swear jar.", "4. Ping your wrist with a rubber band.", "5. Pretend your grandmother is always within earshot.","6. Avoid explicit music and other swear-happy media.", "7. Convince yourself that swearing is a negative thing", "8. Practice positive thinking.", "9. Be patient with yourself.", "10. Pay attention to your swearing habits."]
    else:
        badWordsSummary = ["You have a pretty good record!"]
    return render(request, 'core/home.html', {'badWordsSummary' : badWordsSummary, 'steps' : steps, 'achievement':achievement,'alcohol':alcohol,'clothing':clothing,'cooking':cooking,'family':family,'government':government,'music':music,'party':party,'programming':programming,'science':science,'opennesspositive':opennesspositive,'opennessnegative':opennessnegative,'extrovertpositive':extrovertpositive,'extrovertnegative':extrovertnegative,'neuroticpositive':neuroticpositive,'neuroticnegative':neuroticnegative,'aggreablepositive':aggreablepositive,'aggreablenegative':aggreablenegative,'conscientiousnesspositive':conscientiousnesspositive,'conscientiousnessnegative':conscientiousnessnegative,'anger':anger,'fear':fear,'happiness':happiness,'hate':hate,'love':love,'sad':sad,'surprise':surprise,'worry':worry, 'tweets' : tweets , 'emoji' : emojis, 'MovieSummary' : MovieSummary, 'pos' : pos, 'neg' : neg, 'positiveTweets' : positiveTweets, 'negativeTweets' : negativeTweets , 'likes' : likes, 'dislikes' : dislikes, 'summary' : summary, 'badWordsCount' : badWordsCount, 'percent' : percent, 'maximum' : maximum })


@login_required
def shashank(request):
    return render(request, 'core/textBasedPrediction.html')

@login_required
def newtext(request):
    message = request.POST.get('message')
    newMessage = sent_tokenize(message)
    # RUN THE MODEL HERE!!!!!!!!!!!!!!
    badwords = 0
    #MOVIE SUMMARY
    # MovieSummary = movieSummaryMaker(message)

    #POSITIVE NEGATIVE TWEETS COUNT
    pos, neg, positiveTweets, negativeTweets = posNegCounter(newMessage)

    #HATE LIKE
    likes, dislikes = hateLikeMaker(newMessage)

    #SUMMARY BASED ON TWEET
    summary, badWordsCount, percent, maximum = summaryMaker(newMessage,badwords)
    if badWordsCount > 10:
        badWordsSummary = ["1. Enlist the help of a friend.", "2. Identify your triggers and learn to avoid them.", "3. Use a swear jar.", "4. Ping your wrist with a rubber band.", "5. Pretend your grandmother is always within earshot.","6. Avoid explicit music and other swear-happy media.", "7. Convince yourself that swearing is a negative thing", "8. Practice positive thinking.", "9. Be patient with yourself.", "10. Pay attention to your swearing habits."]
    else:
        badWordsSummary = ["You have a pretty good record!"]


    anger,fear,happiness,hate,love,sad,surprise,worry,opennesspositive,opennessnegative,extrovertpositive,extrovertnegative,neuroticpositive,neuroticnegative,aggreablepositive,aggreablenegative,conscientiousnesspositive,conscientiousnessnegative = classification(newMessage)
    personalityValues = {'anger':anger, 'fear' : fear, 'happiness' : happiness, 'hate' : hate, 'love' : love, 'sad' : sad, 'surprise' : surprise, 'worry' : worry}
    maxOfAll = max(personalityValues, key = personalityValues.get)
    steps = reciprocate(maxOfAll)
    #EXTRA DATA
    achievement,alcohol,clothing,cooking,family,government,music,party,programming,science = getextra(newMessage)
    # return render(request, 'core/test.html', {'anger':anger,'fear':fear,'happiness':happiness,'hate':hate,'love':love,'sad':sad,'surprise':surprise,'worry':worry})
    return render(request, 'core/test.html', {'badWordsSummary' : badWordsSummary, 'steps' : steps, 'achievement':achievement,'alcohol':alcohol,'clothing':clothing,'cooking':cooking,'family':family,'government':government,'music':music,'party':party,'programming':programming,'science':science,'opennesspositive':opennesspositive,'opennessnegative':opennessnegative,'extrovertpositive':extrovertpositive,'extrovertnegative':extrovertnegative,'neuroticpositive':neuroticpositive,'neuroticnegative':neuroticnegative,'aggreablepositive':aggreablepositive,'aggreablenegative':aggreablenegative,'conscientiousnesspositive':conscientiousnesspositive,'conscientiousnessnegative':conscientiousnessnegative,'anger':anger,'fear':fear,'happiness':happiness,'hate':hate,'love':love,'sad':sad,'surprise':surprise,'worry':worry, 'pos' : pos, 'neg' : neg, 'positiveTweets' : positiveTweets, 'negativeTweets' : negativeTweets , 'likes' : likes, 'dislikes' : dislikes, 'summary' : summary, 'badWordsCount' : badWordsCount, 'percent' : percent, 'maximum' : maximum })


@login_required
def settings(request):
    
    urllib.request.urlretrieve("https://twitter.com/"+request.user.username+"/profile_image?size=original", "C:/Users/saumi/OneDrive/Desktop/New folder (2)/Final PROJECT/simple-social-auth/mysite/static/1.jpg")

    user = request.user
	
    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None
    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None
    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'core/settings.html', {
        'github_login': github_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect
    })

@login_required
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'core/password.html', {'form': form})
