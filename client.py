from socket import *

serverName = 'localhost'
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

randomCity = clientSocket.recv(1024).decode()

print("What is the plate code of", randomCity)

cityNameOfUserGuess = ""

while True:
    usersGuess = input("Your guess: ")

    if usersGuess == "END":
        clientSocket.send(usersGuess.encode())
        clientSocket.close()
        break

    clientSocket.send(usersGuess.encode())

    cityNameOfUserGuess = clientSocket.recv(1024).decode()

    if randomCity != cityNameOfUserGuess:
        if cityNameOfUserGuess == "NON_NUMERIC":
            print("You entered a non-numeric value. Game Over.")
            break

        if cityNameOfUserGuess == "NOT_IN_RANGE":
            print("Number exceeds the range. Game Over.")
            break
        print(f"You have entered the plate code of {cityNameOfUserGuess}")
    else:
        print("Correct!")
        break

clientSocket.close()