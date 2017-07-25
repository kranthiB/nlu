import os

from nlu.model import Metadata, Interpreter

class DataRouter(object):
	DEFAULT_MODEL_NAME = "default"
	
	@staticmethod
	def read_model_metadata(model_dir, config):
		if not os.path.isabs(model_dir):
			model_dir = os.path.join(config['path'], model_dir)
		#model_dir = '/Users/prokarma/kumar/workspace/machine-learning/uprr/nlu/model_20170719-200318'
		model_dir = '/Users/prokarma/kumar/workspace/machine-learning/nlu/model_20170724-202625'
		return Metadata.load(model_dir)		

	def __init__(self, config, component_builder):
		self.config = config
		self.component_builder = component_builder
		self.model_store = self.__create_model_store()
		
	def extract(self, data):
		return self.normalise_request_json(data)
		
	def parse(self, data):
		alias = data.get("model") or self.DEFAULT_MODEL_NAME
		model = self.model_store[alias]
		response = model.parse(data['text'], data.get('time', None))
		return response
		
	def normalise_request_json(self, data):
		_data = {}
		_data['text'] = data['q']
		_data['model'] = 'default'
		return _data
		
	def __create_model_store(self):
		model_dict = {self.DEFAULT_MODEL_NAME: self.config.server_model_dirs}
		model_store = {}
		for alias, model_path in list(model_dict.items()):
			model_store[alias] = self.__interpreter_for_model(model_path)
		return model_store
			
	def __interpreter_for_model(self, model_path):
		metadata = DataRouter.read_model_metadata(model_path, self.config)
		return Interpreter.load(metadata, self.config, self.component_builder)