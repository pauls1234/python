import xml.etree.ElementTree as ET

java_bean_name_key = '[name]'
java_class_name_key = '[class_name]'
java_bean_create_instance_key = '[create_new]'
java_class_instance_name_key = '[class_instance_name]'
java_class_property_name_key = '[class_property_name]'
java_class_property_value_key = '[class_property_value]'
java_class_create_instance = '\n\t\t' + java_class_name_key + ' ' + java_class_instance_name_key + ' = new ' + java_class_name_key + '();'
java_class_set_property = '\n\t\t' + java_class_instance_name_key + '.set' + java_class_property_name_key + "(" + java_class_property_value_key + ");"
java_class_return_instance = '\n\t\treturn ' + java_class_instance_name_key + ';'
java_bean_definition = '\t@Bean(name = \"' + java_bean_name_key + '\")\n\t' + java_class_name_key + ' get' + java_class_name_key + '() {' + java_bean_create_instance_key + '\n\t}'

def create_camel_config_java(osgi_config_beans):
    for bean in osgi_config_beans:
        if bean.tag.endswith('bean'):
            print('Creating bean definition')
            create_java_bean_definition(bean)
        elif bean.tag.endswith('reference'):
            #print(create_java_datasource_bean_definition(bean))
            b = 1
    return ""

def create_java_bean_definition(bean):
    bean_name = bean.attrib.get('id')
    java_class_name = get_java_class_name(bean.attrib.get('class'))
    java_class_instance_name = java_class_name[0].lower() + java_class_name[1:]

    new_java_bean_definition = java_bean_definition.replace(java_bean_name_key, bean_name)
    new_java_bean_definition = new_java_bean_definition.replace(java_class_name_key, java_class_name)

    java_bean_create_instance = create_java_class_create_instance_statement(java_class_instance_name, java_class_name)
    
    for child in bean:
        if child.tag.endswith('property'):
            java_bean_create_instance = java_bean_create_instance + create_jave_class_set_property_statement(child, java_class_instance_name)

    java_bean_create_instance = java_bean_create_instance + create_java_class_return_instance_statement(java_class_instance_name)
    #print(java_bean_create_instance)

    new_java_bean_definition = new_java_bean_definition.replace(java_bean_create_instance_key, java_bean_create_instance)
    print(new_java_bean_definition)

    return new_java_bean_definition

def create_java_class_create_instance_statement(java_class_instance_name, java_class_name):
    statement = java_class_create_instance.replace(java_class_name_key, java_class_name)
    statement = statement.replace(java_class_instance_name_key, java_class_instance_name)
    return statement

def create_java_class_return_instance_statement(java_class_instance_name):
    return java_class_return_instance.replace(java_class_instance_name_key, java_class_instance_name)

def create_jave_class_set_property_statement(property, java_class_instance_name) :
    property_name = property.attrib.get('name')
    property_value = property.attrib.get('ref')
    if property_value == None:
        property_value = '\'' + property.attrib.get('value') + '\''

    statement = java_class_set_property.replace(java_class_instance_name_key, java_class_instance_name)
    statement = statement.replace(java_class_property_name_key, property_name)
    statement = statement.replace(java_class_property_value_key, property_value)
    return statement

def create_java_datasource_bean_definition(bean):
    #print("create java datasource bean definition")
    #print(bean.attrib)
    return ""

def get_java_class_name(java_full_class_name):
    tokens = java_full_class_name.split('.')
    return tokens[len(tokens) - 1]