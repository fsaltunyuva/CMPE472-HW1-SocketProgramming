from socket import *  # For connections
import pandas as pd  # For reading file from Excel
import random  # For randomly picking the city

fileName = "plate_list.xlsx"  # Name of the Excel file

dataframe = pd.read_excel(fileName)

serverPort = 12000  # To use unassigned port (choosing above 0-1023)
serverSocket = socket(AF_INET, SOCK_STREAM)  # Creating a socket object and TCP Connection
serverSocket.bind(('', serverPort))  # Binding the server socket to the specified port number
serverSocket.listen(1)  # Setting the server to listen for incoming connections

currentClientCount = 1

print(f"Waiting for {currentClientCount}th client connection")
print("Server waiting for connection...")

cityNames = dataframe["CityName"].tolist()  # Storing 'CityName' column in list
cityNames = [s.strip() for s in cityNames]  # To clear 'xa0''s in city names

plateNumbers = dataframe["PlateNumber"].tolist()  # Storing 'PlateNumber' column in list

while True:
    Flag = True  # To break the outer while loop when client enters 'END'
    connectionSocket, addr = serverSocket.accept()  # Accepting an incoming connection

    print("Client connected from:   " + str(connectionSocket.getsockname()))

    randomCity = random.choice(cityNames)  # Choosing random city to send client

    indexOfRandomCity = cityNames.index(randomCity)  # Getting the index of the random city to get its plate number
    plateNumberOfRandomCity = plateNumbers[indexOfRandomCity]  # Getting the plate number of the chosen random city

    # DEBUG DELETE LATER
    # print(f"Selected city {randomCity}, Plate number of that city is {plateNumberOfRandomCity}")
    # DEBUG DELETE LATER

    connectionSocket.send(randomCity.encode())  # Sending the random city to the client

    while True:
        usersGuess = connectionSocket.recv(1024).decode()  # Receiving the client's guess

        if usersGuess == "END":  # If client enters 'END', break the outer while loop to end the server
            Flag = False  # To break the outer while-loop
            break

        # print("Received from client: " + str(usersGuess))

        if usersGuess != plateNumberOfRandomCity:  # If client's guess is not correct

            if not usersGuess.isnumeric():  # If client's guess is not numeric
                connectionSocket.send("NON_NUMERIC".encode())  # Send 'NON_NUMERIC' to the client
                currentClientCount += 1  # Increment the client count
                print(f"Waiting for {currentClientCount}th client connection")
                print("Server waiting for connection...")
                break

            if int(usersGuess) < 1 or int(usersGuess) > 81:  # If client's guess is out of range
                connectionSocket.send("NOT_IN_RANGE".encode())  # Send 'NOT_IN_RANGE' to the client
                currentClientCount += 1  # Increment the client count
                print(f"Waiting for {currentClientCount}th client connection")
                print("Server waiting for connection...")
                break

            cityNameOfUserGuess = cityNames[int(usersGuess) - 1]  # Getting the name of the city that user guessed (-1 to get the index)

            connectionSocket.send(cityNameOfUserGuess.encode())  # Send the user's wrongly guessed plate number's city name to the client

            print("Received from client: " + str(usersGuess))

    if not Flag: # If client enters 'END', break the outer while loop to end the server
        break

connectionSocket.close()  # Closing the connection