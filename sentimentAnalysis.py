def main():
    from nltk import tokenize
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    from textblob import TextBlob
    import pandas as pd

    compareLibraries = pd.read_csv('data.csv')

    sentiment = SentimentIntensityAnalyzer()

    def getScore(tweet):
        sentences = tokenize.sent_tokenize(tweet)
        total_score = 0.0
        for sentence in sentences:
            score = sentiment.polarity_scores(sentence)
            total_score += score["compound"]
        return total_score

    compareLibraries["VaderScore"] = compareLibraries["Tweets"].apply(getScore)

    def labelSentiment(score):
        if(score >= 0.5):
            return "Very Positive"
        elif(score > 0.05):
            return "Positive"
        elif(score > -0.05 and score < 0.05):
            return "Neutral"
        elif(score < -0.05 and score > -0.5):
            return "Negative"
        else:
            return "Very Negative"

    compareLibraries['VaderSentiment'] = compareLibraries['VaderScore'].apply(
        labelSentiment)

    def getPol(tweet):
        sentences = tokenize.sent_tokenize(tweet)
        total_score = 0.0
        for sentence in sentences:
            score = TextBlob(sentence).sentiment.polarity
            total_score += score
        return total_score

    compareLibraries["TB_Polarity"] = compareLibraries["Tweets"].apply(getPol)

    compareLibraries["TB_sentiment"] = compareLibraries["TB_Polarity"].apply(
        labelSentiment)

    diff_result = pd.DataFrame(
        columns=["Tweets", "__Vader Sentiment__", "__TextBlob Sentiment__"])

    for tweet, vd, tb in zip(compareLibraries["Tweets"], compareLibraries["VaderSentiment"], compareLibraries["TB_sentiment"]):
        if(vd != tb):
            lst = [tweet, vd, tb]
            row = pd.Series(lst, index=diff_result.columns)
            diff_result = diff_result.append(row, ignore_index=True)

    row_count = diff_result.shape[0]

    print("***Comparing Sentiment calculated by VADER library and TextBlob library***\n\n")

    print(diff_result)

    print("\n\nTotal different results : " + str(row_count) + "\n")

    ans = input("Inspect a tweet manually? (Yes/No) ")
    ans = ans.lower()

    while(ans != "no"):
        num = int(input("Enter the row number of the tweet to display "))
        print(diff_result["Tweets"][num])
        ans = input("\nInspect a tweet manually? (Yes/No) ")
        ans = ans.lower()

    input("\n\nThank You!\n\nPress any key to exit")
