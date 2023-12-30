import importlib
import argparse



def load_component(name, settings):
    component_module = importlib.import_module(name)
    # Extract component specific settings
    component_settings_name = name.upper().split('.')[-1]
    component_settings = getattr(settings, component_settings_name, {})

    return component_module, component_settings

def run_component(settings, dpath):
    """Run a single component in the pipeline

    Parameters
    ----------
    settings
        A loaded settings module
        
    dpath: str
        The dotted path to the component
    """
    module, config = load_component(dpath, settings)
    # Execute the component in the pipeline
    module.run(config)


def run_pipeline(settings):
    """Run the full pipeline

    Parameters
    -----------
    settings
        A loaded settings module
    """
    for dpath in settings.PIPELINE: 
        module, config = load_component(dpath, settings)
        # Execute the component in the pipeline
        module.run(config)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run pipeline for processing of tree inventory data for training of DNN")

    parser.add_argument('settings', type=str, help="The dotted path to a settings file")
    parser.add_argument('--component', '-c', type=str, required=False, help="The dotted path to a pipeline component")
    
    args = parser.parse_args()
    vargs = vars(args)
    settings_path = vargs['settings']

    settings = importlib.import_module(settings_path)

    if args.component:
        run_component(settings, vargs['component'])
    else:
        run_pipeline(settings)