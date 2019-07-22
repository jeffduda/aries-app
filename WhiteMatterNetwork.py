from easybayesy import NaiveBayesNetworkNode, NaiveBayesNetwork
import numpy as np
import openpyxl
from openpyxl import Workbook, load_workbook

def WhiteMatterNetwork(): 
   network =  NaiveBayesNetwork(); 

   dx = NaiveBayesNetworkNode('Diagnosis',['ADEM','Adrenoleukodystrophy','CADASIL','CNS_Lymphoma','High_Grade_Glioma','HIV_Encephalopathy','Low_Grade_Glioma','Metastatic_disease','Migraine','Multiple_Sclerosis_active','Multiple_Sclerosis_inactive','Multiple_Sclerosis_tumefactive','Neuromyelitis_Optica','PML','PRES','Susac_Syndrome','SVID','Toxic_Leukoencephalopathy','Vascular']) 
   dx.category='Diagnosis' 
   nDx = 19
   dx.priors = np.array( [0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.054,0.022,0.054,0.054,0.054]) 
   network.add_node(dx) 

   n = NaiveBayesNetworkNode('enhancementRatio',['Large','Small']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.6,0.2,0.2,0.5,0.6,0.2,0.3,0.4,0.2,0.4,0.2,0.5,0.3,0.2,0.2,0.5,0.2,0.2,0.3 ], [ 0.4,0.8,0.8,0.5,0.4,0.8,0.7,0.6,0.8,0.6,0.8,0.5,0.7,0.8,0.8,0.5,0.8,0.8,0.7 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Number',['Single','Multiple']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.4,0.5,0.1,0.4,0.8,0.5,0.9,0.3,0.3,0.2,0.2,0.3,0.5,0.3,0.3,0.3,0.2,0.5,0.3 ], [ 0.6,0.5,0.9,0.6,0.2,0.5,0.1,0.7,0.7,0.8,0.8,0.7,0.5,0.7,0.7,0.7,0.8,0.5,0.7 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('ventVol',['Enlarged','Normal']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.2,0.3,0.5,0.6,0.3,0.7,0.2,0.2,0.3,0.4,0.2,0.2,0.1,0.5,0.3,0.2,0.7,0.3,0.7 ], [ 0.8,0.7,0.5,0.4,0.7,0.3,0.8,0.8,0.7,0.6,0.8,0.8,0.9,0.5,0.7,0.8,0.3,0.7,0.3 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Chronicity',['Acute','Chronic']) 
   n.category = 'Clinical'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.7,0.1,0.5,0.2,0.3,0.3,0.4,0.5,0.4,0.5,0.2,0.5,0.3,0.5,0.8,0.5,0.2,0.5,0.8 ], [ 0.3,0.9,0.5,0.8,0.7,0.7,0.6,0.5,0.6,0.5,0.8,0.5,0.7,0.5,0.2,0.5,0.8,0.5,0.2 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Susceptibility',['Yes','No']) 
   n.category = 'Signal'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.2,0.2,0.2,0.4,0.3,0.3,0.2,0.4,0.1,0.1,0.1,0.2,0.1,0.1,0.2,0.1,0.1,0.2,0.3 ], [ 0.8,0.8,0.8,0.6,0.7,0.7,0.8,0.6,0.9,0.9,0.9,0.8,0.9,0.9,0.8,0.9,0.9,0.8,0.7 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Enhancement',['Yes','None']) 
   n.category = 'Signal'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.8,0.7,0.2,0.9,0.9,0.2,0.4,0.9,0.1,0.9,0.1,0.8,0.3,0.5,0.7,0.2,0.1,0.2,0.5 ], [ 0.2,0.3,0.8,0.1,0.1,0.8,0.6,0.1,0.9,0.1,0.9,0.2,0.7,0.5,0.3,0.8,0.9,0.8,0.5 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Cortex',['Yes','No']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.2,0.5,0.2,0.5,0.8,0.2,0.8,0.6,0.2,0.2,0.2,0.4,0.2,0.6,0.7,0.1,0.1,0.5,0.5 ], [ 0.8,0.5,0.8,0.5,0.2,0.8,0.2,0.4,0.8,0.8,0.8,0.6,0.8,0.4,0.3,0.9,0.9,0.5,0.5 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Symmetry',['Symmetric','Asymmetric']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.5,0.8,0.8,0.5,0.4,0.9,0.2,0.5,0.6,0.5,0.5,0.2,0.7,0.2,0.8,0.6,0.8,0.8,0.6 ], [ 0.5,0.2,0.2,0.5,0.6,0.1,0.8,0.5,0.4,0.5,0.5,0.8,0.3,0.8,0.2,0.4,0.2,0.2,0.4 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Age',['Old','Young','Adult']) 
   n.category = 'Clinical'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.01,0.01,0.1,0.3,0.3,0.1,0.2,0.4,0.1,0.05,0.05,0.01,0.2,0.1,0.2,0.1,0.7,0.3,0.65 ], [ 0.75,0.7,0.4,0.1,0.3,0.5,0.4,0.2,0.5,0.7,0.7,0.8,0.4,0.5,0.5,0.6,0.01,0.3,0.05 ], [ 0.24,0.29,0.5,0.6,0.4,0.4,0.4,0.4,0.4,0.25,0.25,0.19,0.4,0.4,0.3,0.3,0.29,0.4,0.3 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Immunocompromised',['Yes','No']) 
   n.category = 'Clinical'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.1,0.1,0.1,0.6,0.1,0.9,0.1,0.5,0.1,0.3,0.3,0.3,0.2,0.9,0.2,0.1,0.1,0.5,0.1 ], [ 0.9,0.9,0.9,0.4,0.9,0.1,0.9,0.5,0.9,0.7,0.7,0.7,0.8,0.1,0.8,0.9,0.9,0.5,0.9 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Diffusion',['Restricted','Normal']) 
   n.category = 'Signal'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.6,0.7,0.2,0.9,0.7,0.3,0.3,0.5,0.1,0.4,0.1,0.4,0.3,0.7,0.3,0.3,0.1,0.6,0.7 ], [ 0.4,0.3,0.8,0.1,0.3,0.7,0.7,0.5,0.9,0.6,0.9,0.6,0.7,0.3,0.7,0.7,0.9,0.4,0.3 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Anterior_Temporal',['Yes','No']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.2,0.2,0.7,0.2,0.2,0.3,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.3,0.2 ], [ 0.8,0.8,0.3,0.8,0.8,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.8 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('CorpusCallosum',['Yes','No']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.5,0.8,0.5,0.7,0.8,0.4,0.2,0.5,0.3,0.6,0.6,0.5,0.6,0.4,0.2,0.8,0.2,0.8,0.2 ], [ 0.5,0.2,0.5,0.3,0.2,0.6,0.8,0.5,0.7,0.4,0.4,0.5,0.4,0.6,0.8,0.2,0.8,0.2,0.8 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Periventricular',['Yes','No']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.7,0.7,0.7,0.7,0.7,0.7,0.3,0.7,0.7,0.7,0.7,0.7,0.7,0.7,0.5,0.7,0.7,0.7,0.7 ], [ 0.3,0.3,0.3,0.3,0.3,0.3,0.7,0.3,0.3,0.3,0.3,0.3,0.3,0.3,0.5,0.3,0.3,0.3,0.3 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Sex',['Male','Female']) 
   n.category = 'Clincal'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.5,0.8,0.5,0.6,0.55,0.5,0.5,0.5,0.4,0.2,0.2,0.2,0.3,0.5,0.3,0.2,0.5,0.5,0.4 ], [ 0.5,0.2,0.5,0.4,0.45,0.5,0.5,0.5,0.6,0.8,0.8,0.8,0.7,0.5,0.7,0.8,0.5,0.5,0.6 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Prodrome',['Yes','No']) 
   n.category = 'Clinical'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.5,0.2,0.2,0.2,0.2,0.3,0.2,0.2,0.2,0.2,0.2,0.2,0.2,0.3,0.2,0.2,0.2,0.2,0.2 ], [ 0.5,0.8,0.8,0.8,0.8,0.7,0.8,0.8,0.8,0.8,0.8,0.8,0.8,0.7,0.8,0.8,0.8,0.8,0.8 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('T2',['Decreased','Increased','Normal']) 
   n.category = 'Signal'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01 ], [ 0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98,0.98 ], [ 0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01,0.01 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('T1',['Decreased','Increased','Normal']) 
   n.category = 'Signal'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.3,0.4,0.4,0.5,0.4,0.4,0.6,0.3,0.45,0.6,0.35,0.4,0.3,0.6,0.4,0.5,0.4,0.5,0.4 ], [ 0.1,0.2,0.1,0.2,0.4,0.1,0.1,0.4,0.05,0.05,0.05,0.2,0.1,0.1,0.1,0.1,0.1,0.1,0.2 ], [ 0.6,0.4,0.5,0.3,0.2,0.5,0.3,0.3,0.5,0.35,0.6,0.4,0.7,0.3,0.5,0.4,0.5,0.4,0.4 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Mass_effect',['Yes','No']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.2,0.1,0.1,0.5,0.9,0.1,0.5,0.5,0.1,0.1,0.1,0.4,0.1,0.2,0.1,0.1,0.1,0.3,0.2 ], [ 0.8,0.9,0.9,0.5,0.1,0.9,0.5,0.5,0.9,0.9,0.9,0.6,0.9,0.8,0.9,0.9,0.9,0.7,0.8 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Size',['Small','Large','Medium']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.3,0.2,0.2,0.2,0.1,0.2,0.15,0.3,0.7,0.5,0.7,0.1,0.3,0.1,0.1,0.3,0.2,0.1,0.1 ], [ 0.3,0.6,0.5,0.5,0.6,0.5,0.35,0.4,0.1,0.2,0.1,0.5,0.3,0.6,0.4,0.3,0.4,0.6,0.4 ], [ 0.4,0.2,0.3,0.3,0.3,0.3,0.5,0.3,0.2,0.3,0.2,0.4,0.4,0.3,0.5,0.4,0.4,0.3,0.5 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Lobar_Distribution',['Frontal','Temporal','Parietal','Occipital']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.25,0.2,0.4,0.25,0.4,0.25,0.4,0.25,0.4,0.25,0.25,0.25,0.25,0.4,0.05,0.25,0.25,0.25,0.4 ], [ 0.25,0.1,0.4,0.25,0.3,0.25,0.3,0.25,0.25,0.25,0.25,0.25,0.25,0.1,0.1,0.25,0.25,0.25,0.1 ], [ 0.25,0.35,0.1,0.25,0.2,0.25,0.2,0.25,0.25,0.25,0.25,0.25,0.25,0.4,0.25,0.25,0.25,0.25,0.4 ], [ 0.25,0.35,0.1,0.25,0.1,0.25,0.1,0.25,0.1,0.25,0.25,0.25,0.25,0.1,0.6,0.25,0.25,0.25,0.1 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('Juxtacortical',['Yes','No']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.7,0.5,0.8,0.6,0.9,0.8,0.9,0.7,0.8,0.8,0.8,0.8,0.7,0.8,0.9,0.7,0.7,0.8,0.7 ], [ 0.3,0.5,0.2,0.4,0.1,0.2,0.1,0.3,0.2,0.2,0.2,0.2,0.3,0.2,0.1,0.3,0.3,0.2,0.3 ] ]).transpose() 
   network.add_node(n) 

   n = NaiveBayesNetworkNode('lesionExtent',['Limited','Extensive']) 
   n.category = 'Spatial'
   n.parent = 'Diagnosis' 
   n.probs = np.array( [ [ 0.5,0.2,0.2,0.2,0.2,0.2,0.8,0.5,0.9,0.6,0.6,0.3,0.7,0.3,0.5,0.8,0.5,0.2,0.5 ], [ 0.5,0.8,0.8,0.8,0.8,0.8,0.2,0.5,0.1,0.4,0.4,0.7,0.3,0.7,0.5,0.2,0.5,0.8,0.5 ] ]).transpose() 
   network.add_node(n) 

   network.categories = ['Signal', 'Spatial', 'Clinical'] 
   return network
