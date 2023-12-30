import datetime
from pathlib import Path
import pandas as pd
import numpy as np
import scipy
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
from sklearn.utils.validation import _check_feature_names_in
from sklearn.utils.multiclass import is_multilabel, unique_labels
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import ( OneHotEncoder,
    MinMaxScaler, StandardScaler, FunctionTransformer,
)
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer, make_column_transformer, make_column_selector



def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")
    
def log_name(function_transformer, feature_names_in):
    return ['log']

# Transformers 
class MostCommonSpeciesTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, nspecies, feature_names_out='one-to-one'):
        self.nspecies = nspecies
        self.feature_names_out = feature_names_out
    
    def fit(self, X, y=None):
        self.n_features_in_ = X[1]
        unique, counts = np.unique(X, return_counts=True)
        unique_counts = sorted([(u,c) for u,c in zip(unique, counts)], key=lambda x: x[1], reverse=True)
        most_common = [uc[0] for uc in unique_counts[:self.nspecies]]
        self.unique_ = unique
        self.most_common_ = most_common
        return self
    
    def transform(self, X):
        check_is_fitted(self)
        is_least_common = np.all(X != self.most_common_, axis=1) 
        X[is_least_common] = 'other'
        return X

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self)
        return ['species'] #np.array(input_features, dtype=object)
# Pipelines
log_pipeline = make_pipeline(
    SimpleImputer(strategy='median'),
    FunctionTransformer(np.log, inverse_func=np.exp, feature_names_out='one-to-one'),
)

minmax_pipeline = make_pipeline(
    MinMaxScaler(feature_range=(0,1))
)

standard_scaler = make_pipeline(
    StandardScaler()
)

sqrt_pipeline = make_pipeline(
    FunctionTransformer(np.sqrt, inverse_func=np.square, feature_names_out='one-to-one')
)

def species_pipeline(nspecies): 
    return make_pipeline(
    SimpleImputer(strategy='most_frequent'),
    MostCommonSpeciesTransformer(nspecies),
    OneHotEncoder()
)

def run(config):
    report("Commencing data transformation")
    sites = config.get('SITES', [])
    if len(sites) == 0:
        report("No sites provided in settings. Please provide what sites to process.")

    if isinstance(sites, str):
        sites = [sites]

    log_cols = config.get('LOG_COLS', [])
    sqrt_cols = config.get('SQRT_COLS', [])
    minmax_cols = config.get('MINMAX_COLS', [])
    standard_cols = config.get('STANDARD_COLS', [])
    passthrough_cols = config.get('PASSTHROUGH_COLS', [])
    species_cols = config.get('SPECIES_COLS', [])
    nspecies=15

    for site in sites:
        report(f"Starting preparation of traing data {site}")
        for traintest in ('train', 'test'):
            ipath = Path(config['INPUT_PATH'].format(site=site))
            opath = Path(config['OUTPUT_PATH'].format(site=site))
            ifname = Path(config['INPUT_FNAME'].format(site=site, traintest=traintest))
            ofname = Path(config['OUTPUT_FNAME'].format(site=site, traintest=traintest))

            df = pd.read_csv(ipath.joinpath(ifname))

            transformer_pipes = []
            usecols = set(passthrough_cols.copy())
            for column in [ ('log', log_pipeline, log_cols),
                            ('norm', minmax_pipeline, minmax_cols),
                            ('standard', standard_scaler, standard_cols),
                            ('sqrt', sqrt_pipeline, sqrt_cols),
                            ('species', species_pipeline(nspecies), species_cols),
                        ]:
                if len(column[2]) > 0:
                    transformer_pipes.append(column)
                    usecols |= set(column[2])
            
            usecols = list(usecols)
            preprocessing = ColumnTransformer(transformer_pipes, remainder='passthrough')
            trans = preprocessing.fit_transform(df[usecols])
            # We might get back a sparse matrix, so we need to make it a numpy 
            # array for the dataframe
            if isinstance(trans, scipy.sparse._csr.csr_matrix):
                trans = trans.toarray()

            preprocessed_feature_names = preprocessing.get_feature_names_out()
            df_column_names = []
            for name in preprocessed_feature_names:
                tr_kind, n = name.split('__')
                if tr_kind == 'remainder':
                    df_column_names.append(n)
                else:
                    df_column_names.append(name)

            df_trans = pd.DataFrame(trans, columns=df_column_names,
                                    index=df.index)
            

            # Prepare output
            if not opath.exists():
                opath.mkdir(parents=True)

            df_trans.to_csv(opath.joinpath(ofname), index=False)
        
    report("Finished data transformation")