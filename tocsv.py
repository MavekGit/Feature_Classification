
import csv
import numpy as np


def write2csv(number_of_rows,number_of_col):

    row = 0
    col = 0
    #number_of_rows = 8
    #number_of_col = 118
    feature_list = np.empty([number_of_rows,number_of_col], dtype=object)
    txt_file = "C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/data.txt"


    csv_file1 = "C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/cechy.csv"


    # otwórz plik csv do zapisu
    with open(csv_file1, "w", newline='') as outfile:
        

        # stwórz obiekt writer
            
        writer = csv.writer(outfile)


        # otwórz plik txt do odczytu
        with open(txt_file, "r") as infile:

        # wczytaj całą zawartość pliku txt
            text = infile.read()

            # znajdź wszystkie indeksy wystąpień wyrazu
            feature = [i for i in range(len(text)) if text.startswith(": ", i)]        

            
            for i in range(len(feature)):

            # pobierz fragment tekstu dla każdego wyrazu
                feature_clean = text[feature[i]+2:text.find("\n", feature[i])] if i < len(feature) else ""
                feature_list[row][col] = feature_clean
                col += 1
                if col == number_of_col:
                    row += 1
                    col = 0
                if row == number_of_rows:
                    break
            # zapisz wartości do pliku CSV        
            print(feature_list)
            for row in feature_list:        
                writer.writerow(row)
        

    outfile.close()


