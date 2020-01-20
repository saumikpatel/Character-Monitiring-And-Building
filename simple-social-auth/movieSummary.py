import pandas as pd
from nltk.tokenize import word_tokenize
import operator

def movieSummaryMaker(tweets):
    genreScore = {}
    movieNumber = -1
    movieSummary = ""
    for i in tweets:
        # text = "I love the movie Farz"
        textToken = word_tokenize(i)

        csvFile = pd.read_csv('BollywoodMovieDetail.csv')

        title = csvFile['title']

        #Create a list of all movie titles
        movies = []
        for j in title:
            j.lower()
            movies.append(j)

        # We need to split every movie name so as to check its presence (The space between movie names creates a major problem!)
        z=[]
        for j in movies:    
            z.append(word_tokenize(j))

        # Check the presence of each and every tokenized movie name in text
        found=[]
        for j,k in enumerate(z):
            #j = Numbers, k = Values 
            for l in k:
                if l in textToken:
                    found.append(j)
                    break


        f = set(textToken)
        for j in found:
            d = set(z[j])
            if d <= f:
                movieNumber = j
        if movieNumber != -1:
            genre = csvFile['genre'][movieNumber]
            genres = genre.split(" | ")

            for j in genres:
                if j not in genreScore:
                    genreScore[j] = 1
                else:
                    genreScore[j] += 1

    predGenre = max(genreScore.items(), key=operator.itemgetter(1))[0]
    if predGenre == 'Fantasy' or predGenre == 'Sci-Fi':
        movieSummary = '''You like Fantasy or Sci-Fi more! Whether you prefer missions or quests, liking sci-fi or fantasy movies means 
        you believe in magic existing in our mundane world. You're creative and have a vivid imagination, 
        one you use to fully immerse yourself in the faraway world of the movies you love. You know how to 
        think outside of the box and see all the different possibilities our universe have to offer.'''
    elif predGenre == 'Comedy':
        movieSummary = '''People who love comedies are the ones who love to laugh and love to make others 
        laugh, even if that means laughing at themselves. You might run from responsibility at times but it
        doesn't mean you can't be counted on. You know the world can be a tough, harsh place but you choose 
        to look for the fun and the good to make it all more bearable.'''    
    elif predGenre == 'Action' or predGenre == 'Adventure':
        movieSummary = '''Needless to say you love adventure whether it's as a hero saving the day or as a 
        man/woman on a mission. You're brave and believe in fighting for what you want and believe in. You 
        crave excitement and don't mind taking a few risks to find it. You try to live life to it's fullest
        because you know that any day can be your last.'''
    elif predGenre == 'Horror':
        movieSummary = '''If horror is your go-to movie, you clearly have a dark side that you're not afraid
        to embrace. You're blunt and make sure to tell things as you see them and you tend to be more on the 
        pessimistic side. But don't go thinking you're a horrible person! You're strong in the face of any fear 
        you might feel and your friends know that they can always lean on you for support.'''
    elif predGenre == 'Romance':
        movieSummary = '''It isn't that much of a leap to say that you are lovers but that doesn't mean you won't 
        fight-it'll just be for the people and things you love. You are passionate in all areas of your life and 
        always try to make other people happy. You are loyal and compassionate and don't give up easily which only 
        helps to fuel your never-ending hope.'''
    elif predGenre == 'Musical':
        movieSummary = '''ust like musicals can range from the ones that make you laugh to the ones that make you 
        cry, you are full of all different emotions which you have no problem sharing. You're artistic, creative and 
        outgoing and you don't shy away from attention.'''
    elif predGenre == 'Drama':
        movieSummary = '''You like Drama more! It goes with out saying that you have an affinity for the dramatic. You are not afraid 
        to tackle the harsh realities of life but you also can see the wonder that is there. You have a big heart 
        and are supportive of all your friends and family, even if you do sometimes tell them what they don't want 
        to hear.'''
    elif predGenre == 'Animated':
        movieSummary = '''You are definitely a child-at-heart. You know the importance of smiling, laughing, 
        letting loose and just having fun. You're loyal and have no issue with owning your weirdness and being 
        unique. You always think of other people and have a pure heart that many are envious of.'''

    return movieSummary