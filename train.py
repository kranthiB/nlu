import argparse
import logging
import sys
import os

sys.path.insert(0,'/Users/prokarma/kumar/workspace/machine-learning/uprr')

from pkrm_nlu.config import PkrmNLUConfig
from pkrm_nlu.model import Trainer
from pkrm_nlu.converters import load_data

logger = logging.getLogger(__name__)

def create_argparser():
	parser = argparse.ArgumentParser(description='train a custom language parser')
	parser.add_argument('-c', '--config', required=True,
						help="PKRM NLU configuration file")
	parser.add_argument('-m', '--mitie_file', default=None,
						help='File with mitie total_word_feature_extractor')
	return parser
	
def init():
	parser = create_argparser()
	args = parser.parse_args()
	config = PkrmNLUConfig(args.config, os.environ, vars(args))
	return config
	
def do_train(config, component_builder=None):
	trainer = Trainer(config, component_builder)
	persistor = None
	training_data = load_data(config['data'])
	interpreter = trainer.train(training_data)
	persisted_path = trainer.persist(config['path'], persistor, model_name=config['name'])
	return trainer, interpreter, persisted_path

if __name__ == '__main__':
	config = init()
	logging.basicConfig(level=config['log_level'])
	do_train(config)
	logger.info("Finished training")