from gevent.wsgi import WSGIServer
from flask import Flask
from flask import current_app
from flask import jsonify
from flask import request

import logging
import sys
import argparse
import os

sys.path.insert(0,'/Users/prokarma/kumar/workspace/machine-learning/uprr')

from pkrm_nlu.data_router import DataRouter
from pkrm_nlu.config import PkrmNLUConfig

logger = logging.getLogger(__name__)

def create_argparser():
	parser = argparse.ArgumentParser(description='parse incoming text')
	parser.add_argument('-c', '--config',
                        help="config file, all the command line options can also be passed via a (json-formatted) " +
                             "config file. NB command line args take precedence")
	parser.add_argument('-d', '--server_model_dirs',
						help='directory containing model to for parser to use')
	parser.add_argument('-m', '--mitie_file',
						help='file with mitie total_word_feature_extractor')
	return parser

def create_app(config, component_builder=None):
	pkrm_nlu_app = Flask(__name__)
	
	@pkrm_nlu_app.route('/parse', methods = ['GET'])
	def parse():
		request_params = request.args
		data = current_app.data_router.extract(request_params)
		response = current_app.data_router.parse(data)
		return jsonify(response)
	
	pkrm_nlu_app.data_router = DataRouter(config, component_builder)
	return pkrm_nlu_app
		
if __name__ == '__main__':
	arg_parser = create_argparser()
	cmdline_args = {key: val for key, val in list(vars(arg_parser.parse_args()).items()) if val is not None}
	pkrm_nlu_config = PkrmNLUConfig(cmdline_args.get("config"), os.environ, cmdline_args)
	app = WSGIServer(('0.0.0.0', 5000), create_app(pkrm_nlu_config))
	logger.info('Started http server on port 5000')
	app.serve_forever()
	model_20170719-200318