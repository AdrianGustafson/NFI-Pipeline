# Settings file for the NFI data extraction
import os

# Input data path, modify for your local architechture
BASE_DATA_PATH = ''

# Output directory path
STORE_DATA_PATH = os.path.join(BASE_DATA_PATH, 'store_notransform_smote_species')

# What data to use
# 'Full' = all the data including managed plots
# 'Noharvest' = Only reserve data without management
USE_DATA = 'Noharvest'

DEV_SITES = ['RSF', 'NFG', 'NNL', 'NPO', 'NSW']
NFI_SITES = ['NFG', 'NNL', 'NPO',  'NSW', ]
ALL_SITES = ['RSF', 'NFG', 'NNL', 'NPO', 'NSW', 'SLO', 'FRM', 'GEM', 'UKF', 'UKR']
SELECTED_SITES = [ 'NSP', 'RSF', 'NFG', 'NNL', 'NPO']

PIPELINE = [
    'components.extract_noharvest',
    'components.split_dead_alive',
    'components.create_test_set',
    'components.smote_upsampling',
    'components.transform_data',
    'components.append_sites',
    'components.select_columns',
    'components.train_dnn',
    'components.test_dnn'
]

EXTRACT_NOHARVEST = {
    'INPUT_PATH': os.path.join(BASE_DATA_PATH, '{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'OFNAME_BIOMASS': '01_treedata-biomass_TMt_{site}_noharvest.csv',
    'OFNAME_STAND': '02_stand-level-dynamics_TMt_{site}_noharvest.csv',
    'SITES': SELECTED_SITES,
    'STRATEGY': 'plot'
}

SPLIT_DEAD_ALIVE = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'INPUT_FNAME': '01_treedata-biomass_TMt_{site}_noharvest.csv',
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest.csv',
    'SITES': SELECTED_SITES,
}

APPEND_SITES = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_trans_{traintest}.csv',
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, 'appended'),
    'OUTPUT_FNAME': 'tree_biomass_rgr_bounded_noharvest_smote_{traintest}.csv',
    'SITES': NFI_SITES,
    'TRAIN_TEST': ('test', 'train')
}

CREATE_TEST_SET = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest.csv',
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_{traintest}.csv',
    'SITES': SELECTED_SITES,
    'TEST_RATIO': 0.2,
    'STRATIFY': True,
    'STRAT_COL': ['alive', 'species.cor']
}

CONNECT_TRAITS = {
    'INPUT_PATH': os.path.join(BASE_DATA_PATH, 'store','{site}'),
    'INPUT_PATH_TRAIT': os.path.join(BASE_DATA_PATH, '{site}'),
    'OUTPUT_PATH': os.path.join(BASE_DATA_PATH, 'store', '{site}'),
    'SITES': ALL_SITES,
}

SMOTE_UPSAMPLING = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_train.csv',
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_smote_train.csv',
    'SITES': NFI_SITES,
    'VARIABLES': ['gr_r', 'biomass_before_death', 'dt', 'species.cor']
}

TRANSFORM_DATA = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_{traintest}.csv',
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_trans_{traintest}.csv',
    'SITES': NFI_SITES,
    'LOG_COLS': [],
    'SQRT_COLS': [],
    'MINMAX_COLS': [],
    'SPECIES_COLS': ['species.cor'],
    'PASSTHROUGH_COLS': ['tmt.tree.id', 'tmt.plot.id', 'tmt.census.id', 'height2', 'gr_r', 'biomass_before_death', 'dt', 'alive'],
    #'TRAIN_TEST': ['test']
}

SELECT_DATA = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_trans_{traintest}.csv',
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, 'appended'),
    'OUTPUT_FNAME': 'tree_biomass_rgr_bounded_noharvest_smote_{traintest}.csv',
    'TRAIN_TEST': ('train', 'test'),
    'COLS': [
        'gr_r', 'biomass_before_death', 'dt', 
        'species__species_Fagus sylvatica',
 'species__species_Pinus sylvestris',
 'species__species_Picea abies',
 'species__species_Quercus robur',
 'species__species_Abies alba',
 'species__species_Alnus glutinosa',
 'species__species_Salix alba',
 'species__species_Larix kaempferi',
 'species__species_Fraxinus excelsior',
 'species__species_Betula pubescens',
 'species__species_Betula pendula',
 'species__species_Pseudotsuga menziesii',
 'species__species_Tilia cordata',
 'species__species_Pinus nigra',
 'species__species_Acer pseudoplatanus',
 'species__species_Populus tremula',
 'species__species_Ulmus glabra',
 'species__species_Picea sitchensis',
 'species__species_Prunus padus',
 'species__species_Corylus avellana',
 'species__species_Sorbus aucuparia',
 'species__species_Quercus petraea',
 'species__species_Carpinus betulus',
 'species__species_Juniperus oxycedrus',
 'species__species_Juniperus communis',
 'species__species_Quercus spp.',
 'species__species_Pinus spp.',
    ]
}

TRAIN_DNN = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'appended'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, 'artifacts'),
    'TRAIN_INPUT_FNAME': 'tree_biomass_rgr_bounded_noharvest_smote_selected_train.csv',
    'ARTIFACT_NAME': 'DNN4LPJG_input_notrans_smote_species.pt',
    'EPOCHS': 3000,
    'LEARN_RATE': 0.00003,
    'BATCH_SIZE': 512,
    'FEATURES': [
        'gr_r', 'biomass_before_death', 'dt', 
        'species__species_Fagus sylvatica',
        'species__species_Pinus sylvestris',
        'species__species_Picea abies',
        'species__species_Quercus robur',
        'species__species_Abies alba',
        'species__species_Alnus glutinosa',
        #'species__species_Salix alba',
        'species__species_Larix kaempferi',
        'species__species_Fraxinus excelsior',
        'species__species_Betula pubescens',
        'species__species_Betula pendula',
        'species__species_Pseudotsuga menziesii',
        'species__species_Tilia cordata',
        'species__species_Pinus nigra',
        'species__species_Acer pseudoplatanus',
        'species__species_Populus tremula',
        #'species__species_Ulmus glabra',
        #'species__species_Picea sitchensis',
        #'species__species_Prunus padus',
        #'species__species_Corylus avellana',
        'species__species_Sorbus aucuparia',
        'species__species_Quercus petraea',
        'species__species_Carpinus betulus',
        #'species__species_Juniperus oxycedrus',
        #'species__species_Juniperus communis',
        #'species__species_Quercus spp.',
        #'species__species_Pinus spp.',
        #'species__species_Indet spp.'
    ]
}

TEST_DNN = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'appended'),
    'OUTPUT_PATH':os.path.join(STORE_DATA_PATH,'report', 'smote_species'),
    'STATE_PATH': os.path.join(STORE_DATA_PATH, 'artifacts', 'DNN_4_LPJG_input_notrans_smote_species_sklearn.pt'),
    'TEST_DATA_FNAME': 'tree_biomass_rgr_bounded_noharvest_smote_selected_test.csv',
    'FEATURES': [
        'gr_r', 'biomass_before_death', 'dt', 
        'species__species_Fagus sylvatica',
        'species__species_Pinus sylvestris',
        'species__species_Picea abies',
        'species__species_Quercus robur',
        'species__species_Abies alba',
        'species__species_Alnus glutinosa',
        #'species__species_Salix alba',
        'species__species_Larix kaempferi',
        'species__species_Fraxinus excelsior',
        'species__species_Betula pubescens',
        'species__species_Betula pendula',
        'species__species_Pseudotsuga menziesii',
        'species__species_Tilia cordata',
        'species__species_Pinus nigra',
        'species__species_Acer pseudoplatanus',
        'species__species_Populus tremula',
        #'species__species_Ulmus glabra',
        #'species__species_Picea sitchensis',
        #'species__species_Prunus padus',
        #'species__species_Corylus avellana',
        'species__species_Sorbus aucuparia',
        'species__species_Quercus petraea',
        'species__species_Carpinus betulus',
        #'species__species_Juniperus oxycedrus',
        #'species__species_Juniperus communis',
        #'species__species_Quercus spp.',
        #'species__species_Pinus spp.',
        #'species__species_Indet spp.'
], # The number of features the DNN was trained with. Should correspond to FEATURES in TRAIN_DNN
}