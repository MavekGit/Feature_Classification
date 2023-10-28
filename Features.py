from __future__ import print_function
import logging
import SimpleITK as sitk
import radiomics
from radiomics import featureextractor
import cv2
import numpy as np 
import cv2
import tocsv
import time
import warnings


number_of_rows = 0 
def saveToFile(image_sitk,mask_sitk,number_of_rows):
  number_of_col = 118
  # zapis do pliku data.txt
  with open(r"C:/Users/Mavek/Desktop/Magisterka/Prostata_Cechy/data.txt", "a") as f:
    featureVector = extractor.execute(image_sitk, mask_sitk)

    featureVector = {k: featureVector[k] for i, k in enumerate(featureVector) if i >= 11}
    
    for featureName in featureVector.keys():
      #print("Computed %s: %s" % (featureName, featureVector[featureName]))
      f.write("Computed %s: %s\n" % (featureName, featureVector[featureName]))
            
    index_Photo.append(i)
    index_Patient.append(j)
 
    number_of_rows = number_of_rows+1
  #  print(number_of_rows,"wiersze")
  #  print(number_of_col,"kolumny")      
  f.close()  
  return number_of_rows

start_time = time.time()
counter = 0
images = []
masks = []
mask_of_1 = []
mask_of_2 = []
number_of_col = 0
index_Patient = []
index_Photo = []
extractor = featureextractor.RadiomicsFeatureExtractor()
#extractor.disableAllFeatures()

#extractor.settings['force2D'] = True
#extractor.settings['symmetricalGLCM'] = True

extractor.enableAllFeatures()


# inicjalizacja cech pierwszego rzędu
#extractor.enableFeatureClassByName('firstorder')
# inicjalizacja cech drugiego rzędu
#extractor.enableFeatureClassByName('glcm')
# wybór cech chcemy aby program policzył
#extractor.enableFeaturesByName(glcm=['Contrast', 'Correlation','Homogeneity2'])
#extractor.enableFeaturesByName(firstorder=['Mean','Variance' ,'Kurtosis','Skewness','Energy','Entropy'])


# liczba cech mozna liczyczyć za każdym razem ale po co
number_of_col = 118

# czyszczenie pliku data.txt
with open(r"C:/Users/Mavek/Desktop/Magisterka/Prostata_Cechy/data.txt", "w") as f:
    pass
f.close()


# wczytytawnie obrazów j zakres 1-125 i 1-34
for j in range(60,61):
    for i in range(1,34):
        counter = counter+1

        # wczytanie zdjęć medycznych
        imgfilename = r'C:/Users/Mavek/Desktop/Magisterka/Prostata_Cechy/Prostaty_2D_PNG_B08/P_{:03d}_{:04d}.png'.format(j,i)
        image_cv2 = cv2.imread(imgfilename)
        
        # sprawdzenie czy obraz o takiej nazwie istnieje zakładamy że jeśli obraz istnieje to jego maska też 
        if image_cv2 is not None:
          # zamiana obrazu na obiekt typu SimpleITK żeby móc użyć featureextractor.RadiomicsFeatureExtractor()
          image_sitk = sitk.GetImageFromArray(image_cv2)
#          cv2.imshow("obraz"+str(i),image_cv2)
#          images.append(image_sitk)
          maskfilename = r'C:/Users/Mavek/Desktop/Magisterka/Prostata_Cechy/Segmentacje_PNG_B08/P_{:03d}_{:04d}.png'.format(j,i)
          mask_cv2 = cv2.imread(maskfilename)

          
#          cv2.imshow("maska"+str(i),mask_cv2)
          mask_of_1 = np.zeros_like(mask_cv2)
          mask_of_2 = np.zeros_like(mask_cv2)
          mask_of_12 = np.zeros_like(mask_cv2)



          # Zaznaczamy interesującą nas maskę w obrazie po segmentacji
          mask_of_1[mask_cv2 == 0] = 0
          mask_of_1[mask_cv2 == 1] = 1
          mask_of_1[mask_cv2 == 2] = 0

          mask_of_2[mask_cv2 == 0] = 0
          mask_of_2[mask_cv2 == 1] = 0
          mask_of_2[mask_cv2 == 2] = 1

          mask_of_12[mask_cv2 == 0] = 0
          mask_of_12[mask_cv2 == 1] = 1
          mask_of_12[mask_cv2 == 2] = 1

          mask_sitk_of_1 = sitk.GetImageFromArray(mask_of_1)
          mask_sitk_of_2 = sitk.GetImageFromArray(mask_of_2)
          mask_sitk_of_12 = sitk.GetImageFromArray(mask_of_12)

          uni = np.unique(mask_cv2)
          print(uni)




          # Jeśli wektor ma tylko jedną unikalna wartość znaczy że maska zawiera same 0 taki obraz pomijamy
          # if (np.unique(mask_sitk_of_1)).size > 1:

          #   number_of_rows = saveToFile(image_sitk,mask_sitk_of_1,number_of_rows) 

          if (np.unique(mask_sitk_of_2)).size > 1:

            number_of_rows = saveToFile(image_sitk,mask_sitk_of_2,number_of_rows)

          # if (np.unique(mask_sitk_of_12)).size > 1:

          #   number_of_rows = saveToFile(image_sitk,mask_sitk_of_12,number_of_rows)

        else:
           print("Nie znaleziono pliku")

        print("Patient ",j,"Photo ",i)

# zapisz index zdjęcia do odrębnego pliku
with open(r"C:/Users/Mavek/Desktop/Magisterka/Prostata_Cechy/index_Photo.txt", "w") as Photo_file:
    for row in (index_Photo):
      Photo_file.write(str(row)+"\n")
    #print(index_Photo)
Photo_file.close()


# zapisz index pacjęta do odrębnego pliku
with open(r"C:/Users/Mavek/Desktop/Magisterka/Prostata_Cechy/index_Patient.txt", "w") as Patient_file:
    for row in (index_Patient):
      Patient_file.write(str(row)+"\n")
    #print(index_Patient)
Patient_file.close()


cv2.waitKey(0) 
cv2.destroyAllWindows()    
tocsv.write2csv(number_of_rows,number_of_col)
# print(index_Patient)
# print(index_Photo)
print("Process finished --- %s seconds ---" % (time.time() - start_time))