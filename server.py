from socket import *
import pandas as pd
import random

fileName = "plate_list.xlsx"

dataframe = pd.read_excel(fileName)

serverPort = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

currentClientCount = 1

print("Waiting for " + str(currentClientCount) + "th client connection")
print("Server waiting for connection...")

cityNames = dataframe["CityName"].tolist()
cityNames = [s.strip() for s in cityNames] # To clear 'xa0''s in city names

plateNumbers = dataframe["PlateNumber"].tolist()


while True:
    connectionSocket, addr = serverSocket.accept()

    print("Client connected from:   " + str(connectionSocket.getsockname()))

    randomCity = random.choice(cityNames)

    indexOfRandomCity = cityNames.index(randomCity)
    plateNumberOfRandomCity = plateNumbers[indexOfRandomCity]

    print(f"Selected city {randomCity}, Plate number of that city {plateNumberOfRandomCity}")

    connectionSocket.send(randomCity.encode())

    while True:
        usersGuess = connectionSocket.recv(1024).decode()
        print("Received from client: " + str(usersGuess))

        if usersGuess != plateNumberOfRandomCity:
            cityNameOfUserGuess = cityNames[int(usersGuess) - 1]
            print(f"Client's input is the plate number of the city, {cityNameOfUserGuess}")
            connectionSocket.send(cityNameOfUserGuess.strip().encode())

            # # Client exceeds range
            # invalidPlateNumberResponse = "-1"
            # connectionSocket.send(invalidPlateNumberResponse.encode())
            # break

    connectionSocket.close()
