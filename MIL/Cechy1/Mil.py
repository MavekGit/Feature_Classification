import pandas as pd
import numpy as np
import misvm
import math
import mil
from mil.trainer import Trainer
from mil.metrics import AUC
from mil.preprocessing import StandarizerBagsList
from mil.bag_representation import MILESMapping
from mil.validators import LeaveOneOut

from skmultilearn.problem_transform import BinaryRelevance
from sklearn.svm import SVC
from sklearn.multioutput import MultiOutputClassifier
from scipy.sparse import csr_matrix

#DO PRZETESTOWANIA I POPRAWIENIA
label = []
PSA_bags = []
bags = []
veci = []
vecj = []
df = pd.read_csv('C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/MIL/data.txt', sep='\s+', header=None)


index = df.values[:,-1]
index = [int(i) for i in index]  # Przekształcenie wartości index na int

feature = df.values[:,:-1]

unikalne_index = np.unique(index)

# grupowane_dane = [list(feature[index == val]) for val in unikalne_index]
# bags = grupowane_dane

grupowane_dane = [list(feature[index == val].tolist()) for val in unikalne_index]
bags = grupowane_dane


leb = pd.read_csv(r'C:/Users/Maciej Wecki/Desktop/Studia Magisterskie/NTwI/Prostaty/MIL/LABEL.csv', header=None)


for i in range(len(leb.iloc[:, 2])):
    if leb.iloc[i,2] < 3 :
        label.append(1)
        PSA_bags.append(bags[i])
    
    elif leb.iloc[i,2] >= 4:
        label.append(-1)
        PSA_bags.append(bags[i])        

test_label = np.ones(len(bags))
test_label[2] = -1

trainer = Trainer()

# preparing trainer
metrics = ['acc', AUC]
model = SVC(kernel='linear', C=1, class_weight='balanced')
pipeline = [('scale', StandarizerBagsList()), ('disc_mapping', MILESMapping())]
trainer.prepare(model, preprocess_pipeline=pipeline ,metrics=metrics)

valid = LeaveOneOut()
history = trainer.fit(PSA_bags,label,sample_weights='balanced', validation_strategy=valid, verbose=1)


# printing validation results for each fold
print(history['metrics_val'])

# predicting metrics for the test set
trainer.predict_metrics(bags, test_label)

#------------------------------------------------------------------------------------------------------------

# instantiate trainer
PSA_trainer = Trainer()

# preparing trainer
metrics = ['accuracy', 'auc', 'sensibility']  # Poprawione: zmiana 'acc' na 'accuracy'
model = SVC(kernel='linear', C=1, class_weight='balanced')
pipeline = [('scale', StandarizerBagsList()), ('disc_mapping', MILESMapping())]
PSA_trainer.prepare(model, preprocess_pipeline=pipeline, metrics=metrics)

# fitting trainer
valid = LeaveOneOut()
PSA_history = PSA_trainer.fit(PSA_train_bags, PSA_train_label, sample_weights='balanced', validation_strategy=valid, verbose=1)

# printing validation results for each fold

# predicting metrics for the test set
# future = trainer.predict_metrics(bags, PSA_test_label)

PSA_Predict_label = PSA_trainer.predict(bags)

print(PSA_history)

PSA_Predict = PSA_trainer.predict_metrics(bags, PSA_Predict_label)

PSA_history_F1= []  # Dodane: inicjalizacja listy przed pętlą

for i in range(len(PSA_history["accuracy"])):
    # Poprawione: dodanie indeksu 'i' do dostępu do elementów w pętli
    PSA_history_F1.append((2 * (PSA_history['accuracy'][i] * PSA_history['sensibility'][i]) / (PSA_history['accuracy'][i] + PSA_history['sensibility'][i])))

PSA_F1 = []  # Dodane: inicjalizacja listy przed pętlą

for i in range(len(PSA_Predict['accuracy'])):
    # Poprawione: dodanie indeksu 'i' do dostępu do elementów w pętli
    PSA_F1.append((2 * (PSA_Predict['accuracy'][i] * PSA_Predict['sensibility'][i]) / (PSA_Predict['accuracy'][i] + PSA_Predict['sensibility'][i])))

print(PSA_F1)
 