import sys
from socket import *
import pandas as pd
import random

fileName = "plate_list.xlsx"  # Name of the Excel file

dataframe = pd.read_excel(fileName)

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)  # TCP Connection
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

currentClientCount = 1

print(f"Waiting for {currentClientCount}th client connection")
print("Server waiting for connection...")

cityNames = dataframe["CityName"].tolist()  # Storing 'CityName' column in list
cityNames = [s.strip() for s in cityNames]  # To clear 'xa0''s in city names

plateNumbers = dataframe["PlateNumber"].tolist()

while True:
    Flag = True
    connectionSocket, addr = serverSocket.accept()

    print("Client connected from:   " + str(connectionSocket.getsockname()))

    randomCity = random.choice(cityNames)

    indexOfRandomCity = cityNames.index(randomCity)
    plateNumberOfRandomCity = plateNumbers[indexOfRandomCity]

    # DEBUG
    print(f"Selected city {randomCity}, Plate number of that city is {plateNumberOfRandomCity}")

    connectionSocket.send(randomCity.encode())

    while True:
        usersGuess = connectionSocket.recv(1024).decode()

        if usersGuess == "END":
            Flag = False
            break

        print("Received from client: " + str(usersGuess))

        if usersGuess != plateNumberOfRandomCity:
            if not usersGuess.isnumeric():
                connectionSocket.send("NON_NUMERIC".encode())
                currentClientCount += 1
                print(f"Waiting for {currentClientCount}th client connection")
                print("Server waiting for connection...")
                break

            if not usersGuess.isnumeric() or int(usersGuess) < 1 or int(usersGuess) > 81:
                connectionSocket.send("NOT_IN_RANGE".encode())
                currentClientCount += 1
                print(f"Waiting for {currentClientCount}th client connection")
                print("Server waiting for connection...")
                break

            cityNameOfUserGuess = cityNames[int(usersGuess) - 1]  # -1 to get the index (1-1 to get Adana)
            print(f"Client's input is the plate number of the city, {cityNameOfUserGuess}")
            connectionSocket.send(cityNameOfUserGuess.strip().encode())

    if not Flag:
        break

connectionSocket.close()