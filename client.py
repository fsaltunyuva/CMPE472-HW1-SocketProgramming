from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# sentence = input("Input lowercase sentence:")

# clientSocket.send(sentence.encode())
# modifiedSentence = clientSocket.recv(1024)

randomCity = clientSocket.recv(1024).decode()

print("What is the plate code of", randomCity)

cityNameOfUserGuess = ""

while cityNameOfUserGuess != "END":
    usersGuess = input("Your guess: ")
    clientSocket.send(usersGuess.encode())

    cityNameOfUserGuess = clientSocket.recv(1024).decode()

    if randomCity != cityNameOfUserGuess:
        print(f"You have entered the plate code of {cityNameOfUserGuess}")
    elif cityNameOfUserGuess == "-1":
        print("Number exceeds the range. Game Over.")


clientSocket.close()