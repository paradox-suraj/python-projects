from textblob import TextBlob  # importing the TextBlob library

t = 1
while t:
    a = input("Enter the word to be checked: ")  # accepting input from the user
    print("Original text: " + str(a))  # printing the original text

    b = TextBlob(a)  # creating a TextBlob object with the input text

    # printing the corrected spelling
    print("Corrected text: " + str(b.correct()))
    
    t = int(input("Try Again? 1: Yes, 0: No "))  # asking the user if they want to try again
