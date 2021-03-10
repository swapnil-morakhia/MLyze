from textblob import TextBlob

def analyze_text(text):
    text_blob = TextBlob(text)
    analysis = {'sentences': dict(), 'entities': dict()}

    for sentence in text_blob.sentences:
        analysis['sentences'][sentence.string] = sentence.sentiment.polarity

    for index, entity in enumerate(text_blob.noun_phrases):
        analysis['entities'][index] = entity

    print(analysis)

analyze_text('I love how Messi dribbles. I hate how Cristiano dribbles.')
