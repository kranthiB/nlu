import os

__version__ = 1.0

def lazyproperty(fn):
	attr_name = '_lazy_' + fn.__name__
	@property
	def _lazyprop(self):
		if not hasattr(self, attr_name):
			setattr(self, attr_name, fn(self))
		return getattr(self, attr_name)
	return _lazyprop
	
def ordered(obj):
	if isinstance(obj, dict):
		return sorted((k, ordered(v)) for k, v in obj.items())
	if isinstance(obj, list):
		return sorted(ordered(x) for x in obj)
	else:
		return obj
		
def list_to_str(l, delim=", ", quote="'"):
	return delim.join([quote + e + quote for e in l])
	
def create_dir(dir_path):
	try:
		os.makedirs(dir_path)
	except OSError as e:
		if e.errno != errno.EEXIST:
			raise
		
def recursively_find_files(resource_name):
	if not resource_name:
		raise ValueError("Resource name '{}' must be an existing directory or file.".format(resource_name))
	elif os.path.isfile(resource_name):
		return [resource_name]
	elif os.path.isdir(resource_name):
		resources = []
		nodes_to_visit = [resource_name]
		while len(nodes_to_visit) > 0:
			nodes_to_visit = [f for f in nodes_to_visit if not f.split("/")[-1].startswith('.')]
			current_node = nodes_to_visit[0]
			if os.path.isdir(current_node):
				nodes_to_visit += [os.path.join(current_node, f) for f in os.listdir(current_node)]
			else:
				resources += [current_node]
			nodes_to_visit = nodes_to_visit[1:]
		return resources
	else:
		raise ValueError("Could not locate the resource '{}'.".format(os.path.abspath(resource_name)))