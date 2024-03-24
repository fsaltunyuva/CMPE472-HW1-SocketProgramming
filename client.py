from socket import *  # For connections

serverName = 'localhost'
serverPort = 12000  # Port number of the server

clientSocket = socket(AF_INET, SOCK_STREAM)  # Creating a socket object and TCP Connection
clientSocket.connect((serverName, serverPort))  # Connecting to the server

randomCity = clientSocket.recv(1024).decode()  # Receiving the random city from the server

print("What is the plate code of", randomCity)

while True:
    usersGuess = input("Your guess: ")

    if usersGuess == "END":  # If user enters 'END', send 'END' to the server and close the connection
        clientSocket.send(usersGuess.encode())
        clientSocket.close()
        break

    clientSocket.send(usersGuess.encode())  # Sending the user's guess to the server

    cityNameOfUserGuess = clientSocket.recv(1024).decode()  # Receiving the city name of the user's guess

    if randomCity != cityNameOfUserGuess:
        if cityNameOfUserGuess == "NON_NUMERIC":  # If user enters a non-numeric value
            print("You entered a non-numeric value. Game Over.")
            break

        if cityNameOfUserGuess == "NOT_IN_RANGE":  # If user enters a value out of range
            print("Number exceeds the range. Game Over.")
            break

        print(f"You have entered the plate code of {cityNameOfUserGuess}")  # If user enters a wrong value inform the user about their input
    else:  # If user enters the correct value
        print("Correct!")
        break

clientSocket.close()  # Closing the connection