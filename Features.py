from __future__ import print_function
import logging
import SimpleITK as sitk
import radiomics
from radiomics import featureextractor
import cv2
import numpy as np
import cv2
import tocsv
counter = 0
images = []
masks = []
mask_of_1 = []
mask_of_2 = []
number_of_rows = 0
number_of_col = 0
extractor = featureextractor.RadiomicsFeatureExtractor()
#extractor.disableAllFeatures()

extractor.enableAllFeatures()
# inicjalizacja cech pierwszego rzędu
#extractor.enableFeatureClassByName('firstorder')
# inicjalizacja cech drugiego rzędu
#extractor.enableFeatureClassByName('glcm')
# wybór cech chcemy aby program policzył
#extractor.enableFeaturesByName(glcm=['Contrast', 'Correlation','Homogeneity2'])
#extractor.enableFeaturesByName(firstorder=['Mean','Variance' ,'Kurtosis','Skewness','Energy','Entropy'])

# czyszczenie pliku data.txt
with open("C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/data.txt", "w") as f:
    pass
f.close()
# wczytytawnie obrazów j zakres 1-125 i 1-34
for j in range(1,2):
    for i in range(1, 34):

        # wczytanie zdjęć medycznych
        imgfilename = 'C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/Prostaty_2D_PNG_B08/P_{:03d}_{:04d}.png'.format(j,i)
        image_cv2 = cv2.imread(imgfilename)
        
        # sprawdzenie czy obraz o takiej nazwie istnieje zakładamy że jeśli obraz istnieje to jego maska też 
        if image_cv2 is not None:
          # zamiana obrazu na obiekt typu SimpleITK żeby móc użyć featureextractor.RadiomicsFeatureExtractor()
          image_sitk = sitk.GetImageFromArray(image_cv2)
#          cv2.imshow("obraz"+str(i),image_cv2)
#          images.append(image_sitk)
          maskfilename = 'C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/Segmentacje_PNG_B08/P_{:03d}_{:04d}.png'.format(j,i)
          mask_cv2 = cv2.imread(maskfilename)

          
#          cv2.imshow("maska"+str(i),mask_cv2)
          mask_of_1 = np.zeros_like(mask_cv2)
          mask_of_2 = np.zeros_like(mask_cv2)

          # Zaznaczamy interesującą nas maskę w obrazie po segmentacji
          mask_of_1[mask_cv2 == 0] = 0
          mask_of_1[mask_cv2 == 1] = 1
          mask_of_1[mask_cv2 == 2] = 0

          mask_of_2[mask_cv2 == 0] = 0
          mask_of_2[mask_cv2 == 1] = 0
          mask_of_2[mask_cv2 == 2] = 1



          mask_sitk_of_1 = sitk.GetImageFromArray(mask_of_1)
          mask_sitk_of_2 = sitk.GetImageFromArray(mask_of_2)
#          masks.append(mask_sitk)

          uni = np.unique(mask_cv2)
#          print(uni)
#          print("------")
#          print(np.unique(mask_sitk_of_1))
#          print("------")
#          print(np.unique(mask_sitk_of_2))
#          print("------")
          
          # Jeśli wektor ma tylko jedną unikalna wartość znaczy że maska zawiera same 0 taki obraz pomijamy
          if (np.unique(mask_sitk_of_1)).size > 1:
            counter = counter+1
            # zapis do pliku data.txt
            with open("C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/data.txt", "a") as f:
              # Oblicz cechy na podstawie obrazu wyjściowego i jego maski
              # Maska musi być obrazem binarnym gdzie 1 oznacza obszar po etykietowaniu
              # Jeśli w obrazie mamy więcej wartości to cechy zostaną policzone dla maski z wartościami 1
              featureVector = extractor.execute(image_sitk, mask_sitk_of_1)

              featureVector = {k: featureVector[k] for i, k in enumerate(featureVector) if i >= 11}

              for featureName in featureVector.keys():
                print("Computed %s: %s" % (featureName, featureVector[featureName]))
                f.write("Computed %s: %s\n" % (featureName, featureVector[featureName]))
                #umber_of_col = number_of_col + 1 cech jest 118
                
              number_of_rows = number_of_rows+1 
            f.close()
          # Jeśli wektor ma tylko jedną unikalna wartość znaczy że maska zawiera same 0 taki obraz pomijamy
          if (np.unique(mask_sitk_of_2)).size > 1:
            
            # zapis do pliku data.txt
            with open("C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/data.txt", "a") as f:
              featureVector = extractor.execute(image_sitk, mask_sitk_of_2)

              featureVector = {k: featureVector[k] for i, k in enumerate(featureVector) if i >= 11}
              
              for featureName in featureVector.keys():
                print("Computed %s: %s" % (featureName, featureVector[featureName]))
                f.write("Computed %s: %s\n" % (featureName, featureVector[featureName]))
                
                
                
              number_of_rows = number_of_rows+1
              print(number_of_rows,"wiersze")
              print(number_of_col,"kolumny")
              number_of_col = 118
            f.close()  
        else:
           print("Nie znaleziono pliku")
        #print(counter)




cv2.waitKey(0) 
cv2.destroyAllWindows()    
tocsv.write2csv(number_of_rows,number_of_col)

