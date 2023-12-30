# Settings file for the NFI data extraction
import os

# Input data path, modify for your local architechture
BASE_DATA_PATH = ''

# Output directory path
STORE_DATA_PATH = os.path.join(BASE_DATA_PATH, 'store_trans_smote_species')

# What data to use
# 'Full' = all the data including managed plots
# 'Noharvest' = Only reserve data without management
USE_DATA = 'Noharvest'

DEV_SITES = ['UKR', 'UKF', 'RSF', 'SLO', 'GEM', 'FRM',]
SITES = ['RSF', 'NFG', 'NNL', 'NPO', 'NSW', 'FRM', 'GEM', 'SLO', 'UKF', 'UKR']

PIPELINE = [
    'components.create_test_set',
    'components.transform_data',
    'components.smote_upsampling',
    'components.append_sites',
    'components.train_dnn',
    'components.test_dnn'
]

APPEND_SITES = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_trans_{traintest}.csv',
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, 'appended'),
    'OUTPUT_FNAME': 'tree_biomass_rgr_bounded_noharvest_smote_{traintest}.csv',
    'SITES': DEV_SITES,
    'TRAIN_TEST': ('test', 'train')
}

CREATE_TEST_SET = {
    'INPUT_PATH': os.path.join(BASE_DATA_PATH, 'store_base','{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest.csv',
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_{traintest}.csv',
    'SITES': SITES,
    'TEST_RATIO': 0.2,
    'STRATIFY': True,
    'STRAT_COL': ['alive', 'species.cor']
}

CONNECT_TRAITS = {
    'INPUT_PATH': os.path.join(BASE_DATA_PATH, 'store','{site}'),
    'INPUT_PATH_TRAIT': os.path.join(BASE_DATA_PATH, '{site}'),
    'OUTPUT_PATH': os.path.join(BASE_DATA_PATH, 'store', '{site}'),
    'SITES': SITES,
}

SMOTE_UPSAMPLING = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_trans_train.csv',
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_smote_train.csv',
    'SITES': DEV_SITES,
    'VARIABLES': ['sqrt__gr_r', 'log__biomass_before_death', 'norm__dt', 'species__*']
}

TRANSFORM_DATA = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_train.csv',
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_trans_train.csv',
    'SITES': SITES,
    'LOG_COLS': ['biomass_before_death'],
    'SQRT_COLS': ['gr_r', 'biomass_before_death'],
    'MINMAX_COLS': ['dt', 'height2'],
    'SPECIES_COLS': ['species.cor'],
    'PASSTHROUGH_COLS': ['tmt.tree.id', 'tmt.plot.id', 'tmt.census.id', 'alive']
}

TRAIN_DNN = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'appended'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, 'artifacts'),
    'TRAIN_INPUT_FNAME': 'tree_biomass_rgr_bounded_noharvest_smote_train.csv',
    'ARTIFACT_NAME': 'DNN_4_LPJG_input_trans_smote_species_sigmoid_sklearn.pt',
    'EPOCHS': 3000,
    'LEARN_RATE': 0.00003,
    'BATCH_SIZE': 512,
    'FEATURES': [
        'sqrt__gr_r', 
        'log__biomass_before_death', 
        'norm__dt', 

        'species__species_Fagus sylvatica', 'species__species_Picea abies',
        'species__species_Alnus glutinosa', 'species__species_Abies alba',
        'species__species_Betula pubescens',
        'species__species_Pinus sylvestris', 'species__species_Larix kaempferi',
        'species__species_Quercus robur', 'species__species_Fraxinus excelsior',
        'species__species_Pseudotsuga menziesii',
        'species__species_Pinus nigra', 'species__species_Betula pendula',
        'species__species_Tilia cordata', 'species__species_Salix alba',
        'species__species_Picea sitchensis', 'species__species_Ilex aquifolium',
        'species__species_Quercus indet', 'species__species_Quercus petraea',
        'species__species_Acer campestre', 'species__species_Fagus sylvatica ',
        'species__species_Acer pseudoplatanus',
        'species__species_Crataegus monogyna',
        'species__species_Corylus avellana', 'species__species_Acer opalus',
        'species__species_Quercus rubra'

        # 'species__species_Alnus glutinosa',
        # 'species__species_Betula pendula',
        # 'species__species_Betula pubescens',
        # 'species__species_Fagus sylvatica',
        # 'species__species_Ilex aquifolium',
        # 'species__species_Larix kaempferi',
        # 'species__species_Picea abies',
        # 'species__species_Picea sitchensis',
        # 'species__species_Pinus nigra',
        # 'species__species_Pinus sylvestris',
        # 'species__species_Pseudotsuga menziesii',
        # 'species__species_Quercus petraea',
        # 'species__species_Quercus robur',
        # 'species__species_Quercus rubra',
        # 'species__species_Salix alba',
        # 'species__species_other',
        # 'species__species_Abies alba',
        # 'species__species_Acer pseudoplatanus',
        # 'species__species_Carpinus betulus',
        # 'species__species_Fraxinus excelsior',
        # 'species__species_Larix decidua',
        # 'species__species_Populus tremula',
        # 'species__species_Acer indet',
        # 'species__species_Betula indet',
        # 'species__species_Pinus pinaster',
        # 'species__species_Populus indet',
        # 'species__species_Quercus indet',
        # 'species__species_Tilia cordata',
        # 'species__species_Acer platanoides',
        # 'species__species_Alnus incana',
        # 'species__species_Indet indet',
        # 'species__species_Pinus contorta',
        # 'species__species_Salix caprea',
        # 'species__species_Sorbus aucuparia'
 ],   
}

TEST_DNN = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'appended'),
    'OUTPUT_PATH':os.path.join(STORE_DATA_PATH,'report', 'sigmoid'),
    'STATE_PATH': os.path.join(STORE_DATA_PATH, 'artifacts', 'DNN_4_LPJG_input_trans_smote_species_sigmoid_sklearn.pt'),
    'TEST_DATA_FNAME': 'tree_biomass_rgr_bounded_noharvest_smote_test.csv',
    'FEATURES': [
        'sqrt__gr_r', 
        'log__biomass_before_death', 
        'norm__dt', 

        'species__species_Fagus sylvatica', 'species__species_Picea abies',
        'species__species_Alnus glutinosa', 'species__species_Abies alba',
        'species__species_Betula pubescens',
        'species__species_Pinus sylvestris', 'species__species_Larix kaempferi',
        'species__species_Quercus robur', 'species__species_Fraxinus excelsior',
        'species__species_Pseudotsuga menziesii',
        'species__species_Pinus nigra', 'species__species_Betula pendula',
        'species__species_Tilia cordata', 'species__species_Salix alba',
        'species__species_Picea sitchensis', 'species__species_Ilex aquifolium',
        'species__species_Quercus indet', 'species__species_Quercus petraea',
        'species__species_Acer campestre', 'species__species_Fagus sylvatica ',
        'species__species_Acer pseudoplatanus',
        'species__species_Crataegus monogyna',
        'species__species_Corylus avellana', 'species__species_Acer opalus',
        'species__species_Quercus rubra'

        # 'species__species_Alnus glutinosa',
        # 'species__species_Betula pendula',
        # 'species__species_Betula pubescens',
        # 'species__species_Fagus sylvatica',
        # 'species__species_Ilex aquifolium',
        # 'species__species_Larix kaempferi',
        # 'species__species_Picea abies',
        # 'species__species_Picea sitchensis',
        # 'species__species_Pinus nigra',
        # 'species__species_Pinus sylvestris',
        # 'species__species_Pseudotsuga menziesii',
        # 'species__species_Quercus petraea',
        # 'species__species_Quercus robur',
        # 'species__species_Quercus rubra',
        # 'species__species_Salix alba',
        # 'species__species_other',
        # 'species__species_Abies alba',
        # 'species__species_Acer pseudoplatanus',
        # 'species__species_Carpinus betulus',
        # 'species__species_Fraxinus excelsior',
        # 'species__species_Larix decidua',
        # 'species__species_Populus tremula',
        # 'species__species_Acer indet',
        # 'species__species_Betula indet',
        # 'species__species_Pinus pinaster',
        # 'species__species_Populus indet',
        # 'species__species_Quercus indet',
        # 'species__species_Tilia cordata',
        # 'species__species_Acer platanoides',
        # 'species__species_Alnus incana',
        # 'species__species_Indet indet',
        # 'species__species_Pinus contorta',
        # 'species__species_Salix caprea',
        # 'species__species_Sorbus aucuparia'
 ], # The number of features the DNN was trained with. Should correspond to FEATURES in TRAIN_DNN
}