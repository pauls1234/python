from osgi_config_reader import *
from create_camel_config_java import *

osgi_config_file = "resources\\OSGI-INF\\blueprint\\osgi-config.xml"
osgi_config = get_osgi_config(osgi_config_file)
print("a")
osgi_package_name = get_osgi_package_name(osgi_config)
print("b")
osgi_config_beans = get_osgi_config_beans(osgi_config)
print("c")
create_camel_config_java(osgi_config_beans)
