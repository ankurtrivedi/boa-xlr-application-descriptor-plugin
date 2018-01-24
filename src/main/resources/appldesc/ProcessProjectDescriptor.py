#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
#import json
import yaml
from xlrelease.HttpRequest import HttpRequest
from com.xebialabs.xlrelease.api.v1.forms import Variable

MAP_VARIABLE_TYPE = 'xlrelease.MapStringStringVariable'
STRING_VARIABLE_TYPE = 'xlrelease.StringVariable'

def new_variable(name, value, type, required=False, label=None, description=None):
    # setting a dummy value since we can only pass a string here
    variable = Variable(name, None, required)
    variable.setType(type)
    variable.setValue(value)
    if label:
        variable.setLabel(label)
    if description:
        variable.setDescription(description)
    return variable

def create_variable(variableName, variableValue, variableType):
    if variableName in release.getVariablesByKeys():
        print "Variable [%s] already present." % variableName
        var = release.getVariablesByKeys()[variableName]
        var.setValue(variableValue)
        releaseApi.updateVariable(var)
    else:
        print "Adding [%s] variable" % variableName
        var = new_variable(variableName, variableValue,
                           variableType,
                           False, variableName,
                           'The variable %s' % variableName)
        releaseApi.createVariable(release.getId(), var)

if server is None:
    print "No server provided."
    sys.exit(1)

request = HttpRequest(server, None , None)
response = request.get(uri, contentType=contentType)

if not response.isSuccessful():
    print "Failed to retrieve app descriptor from %s/%s" % (server['url'], uri)
    response.errorDump()
    sys.exit(1)
else:
    jsonData= yaml.load(response.getResponse())
    project = jsonData['CDProperties']['project']
    sitinfrastructure= jsonData['CDProperties']['sitinfrastructure']
    patinfrastructure= jsonData['CDProperties']['patinfrastructure']
    prodinfrastructure= jsonData['CDProperties']['prodinfrastructure']
    #applicationPackaging = jsonData['CDProperties']['applicationPackaging']
    #reuseInfraVal = jsonData['CDProperties']['reuseInfra']

    for key in project.keys():
        create_variable(key, project[key], STRING_VARIABLE_TYPE)


    for infra in sitinfrastructure:
        create_variable(infra['envName'], infra, MAP_VARIABLE_TYPE)


    for infra in patinfrastructure:
        create_variable(infra['envName'], infra, MAP_VARIABLE_TYPE)


    for infra in prodinfrastructure:
        create_variable(infra['envName'], infra, MAP_VARIABLE_TYPE)

    #create_variable('reuseInfra',reuseInfraVal,STRING_VARIABLE_TYPE)

    #create_variable('DAR',applicationPackaging,MAP_VARIABLE_TYPE)

    print "Retrieved app Descriptor from %s/%s" % (server['url'], uri)
