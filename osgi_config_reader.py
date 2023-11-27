import os
import xml.etree.ElementTree as ET

def read_osgi_config(file):
    tree = ET.parse(file)
    return tree.getroot()

def get_file_path(file):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, file)
    return file_path

def get_filtered_elements(root, tag_filters):
    elements = []
    for child in root:
        for tag_filter in tag_filters:
            if child.tag.endswith(tag_filter): 
                elements.append(child)
                break
    return elements

def get_project_package_name(camel_context):
    for child in camel_context:
        if child.tag.endswith('packageScan'):
            for packageScanChild in child:
                if packageScanChild.tag.endswith('package'):
                    return packageScanChild.text.replace('.route', '')
    return None

def parse_osgi_project_package_name(project_package_name):
    tokens = project_package_name.split('.')
    return tokens[0] + '.' + tokens[1]

def get_filtered_elements_with_package_name(objs, package_names):
    elements = []
    for obj in objs:
        attr_key = 'class'
        if (obj.tag.endswith('reference')):
            attr_key = 'interface'
        for package_name in package_names:
            result = obj.attrib.get(attr_key)
            if result != None and result.startswith(package_name):
                elements.append(obj)
                break
    return elements

def print_elements(elements):
    for element in elements:
        print(element.tag, element.attrib)

def get_osgi_config(osgi_config_file):
    return read_osgi_config(get_file_path(osgi_config_file))

def get_osgi_config_beans(osgi_config):
    camel_context_tag_filters = []
    camel_context_tag_filters.append('camelContext')
    camel_contexts = get_filtered_elements(osgi_config, camel_context_tag_filters)
    osgi_project_package_name = parse_osgi_project_package_name(get_project_package_name(camel_contexts[0]))

    element_tag_filters = []
    element_tag_filters.append('bean')
    element_tag_filters.append('reference')
    elements = get_filtered_elements(osgi_config, element_tag_filters)

    project_package_names = []
    project_package_names.append(osgi_project_package_name)
    project_package_names.append("javax.sql")
    return get_filtered_elements_with_package_name(elements, project_package_names)

def get_osgi_package_name(osgi_config):

    camel_context_tag_filters = []
    camel_context_tag_filters.append('camelContext')
    camel_contexts = get_filtered_elements(osgi_config, camel_context_tag_filters)
    return get_project_package_name(camel_contexts[0])

#osgi_config_file = "resources\\OSGI-INF\\blueprint\\osgi-config.xml"
#osgi_config = get_osgi_config(osgi_config_file)

#package_name = get_osgi_package_name(osgi_config)
#print('package name:', package_name)

#beans = get_osgi_config_beans(osgi_config)
#print('osgi beans:')
#print_elements(beans)
