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
import json
#import yaml
from xlrelease.HttpRequest import HttpRequest
from com.xebialabs.xlrelease.api.v1.forms import Variable

MAP_VARIABLE_TYPE = 'xlrelease.MapStringStringVariable'
STRING_VARIABLE_TYPE = 'xlrelease.StringVariable'
LIST_VARIABLE_TYPE = 'xlrelease.ListStringVariable'

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

def update_template_variable(variableName, variableValue, variableType,templateId):
    for variable in templateApi.getVariables(templateId):
        print variable.getKey()
        if variable.getKey()== variableName:
            print "Variable [%s] already present. Updating" % variable.getKey()
            if variableType == LIST_VARIABLE_TYPE:
                print "Variable value for list [%s]" % variableValue
                variable.setValue(variableValue)
            elif variableType == MAP_VARIABLE_TYPE:
                print "Variable value for map [%s]" % variableValue
                variable.setValue(variableValue)
            else:
                print "Variable value for string [%s]" % variableValue
                variable.setValue(variableValue)

            templateApi.updateVariable(variable)

def update_release_variable(variableName, variableValue, variableType):
    if variableName in release.getVariablesByKeys():
        print "Variable [%s] already present." % variableName
        var = release.getVariablesByKeys()[variableName]
        var.setValue(variableValue)
        releaseApi.updateVariable(var)

if server is None:
    print "No server provided."
    sys.exit(1)

request = HttpRequest(server, username, password)
response = request.get(uri, contentType=contentType)
jsonData = {}

if not response.isSuccessful():
    print "Failed to retrieve app descriptor from %s/%s" % (server['url'], uri)
    response.errorDump()
    sys.exit(1)
else:
    jsonData= json.loads(response.getResponse())

templateId = getCurrentRelease().getOriginTemplateId()
print templateId

# Update template variables
print "#######################################"
print "Updating Template Variables"

for var in jsonData:
    if type(jsonData[var]) is list:
        print "%s is list Variable" % (var)
        print "Value from Bitbucket is %s" % (jsonData[var])
        update_template_variable(var, jsonData[var], LIST_VARIABLE_TYPE,templateId)
    elif type(jsonData[var]) is dict:
        print "%s is dict Variable" % (var)
        print "Value from Bitbucket is %s" % (jsonData[var])
        update_template_variable(var, jsonData[var], MAP_VARIABLE_TYPE,templateId)
    else:
        print "%s is string Variable" % (var)
        print "Value from Bitbucket is %s" % (jsonData[var])
        update_template_variable(var, jsonData[var], STRING_VARIABLE_TYPE,templateId )

print "Updated Template Variables"
print "#######################################"

# Update release variables
print "#######################################"
print "Updating Release Variables"

for var in jsonData:
    if type(jsonData[var]) is list:
        print "%s is list Variable" % (var)
        print "Value from Bitbucket is %s" % (jsonData[var])
        update_release_variable(var, jsonData[var], LIST_VARIABLE_TYPE)
    elif type(jsonData[var]) is dict:
        print "%s is dict Variable" % (var)
        print "Value from Bitbucket is %s" % (jsonData[var])
        update_release_variable(var, jsonData[var], MAP_VARIABLE_TYPE)
    else:
        print "%s is string Variable" % (var)
        print "Value from Bitbucket is %s" % (jsonData[var])
        update_release_variable(var, jsonData[var], STRING_VARIABLE_TYPE)

print "Updated Release Variables"
print "#######################################"


print "Retrieved app Descriptor from %s/%s" % (server['url'], uri)

