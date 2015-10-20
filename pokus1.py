import urllib2
import json

import pytoml as toml

cofig_file_path = 'config.toml'
config = {}



if __name__ == '__main__':
	with open(config_file_path) as config_file:
		config = toml.load(config_file)
