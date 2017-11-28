#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
from com.xebialabs.deployit.plugin.api.reflect import Type
from com.xebialabs.xlrelease.api.v1.forms import Variable

def new_variable(name, value, valueProvider, type, required=False, label=None, description=None):
    # setting a dummy value since we can only pass a string here
    variable = Variable(name, None, required)
    variable.setType(type)
    variable.setValue(value)
    if valueProvider:
        variable.setValueProvider(valueProvider)
    if label:
        variable.setLabel(label)
    if description:
        variable.setDescription(description)
    return variable

varList = []
USER_INPUT_TASK_TITLE = 'Gate Task'
REPEAT_USING_VARIABLE = 'ComponentList'
for componentName in releaseVariables[REPEAT_USING_VARIABLE]:


    if not componentName.endswith("Composite"):
        #Create a list box variable to put on the User Input task.
        vp = Type.valueOf('xlrelease.ListOfStringValueProviderConfiguration').descriptor.newInstance(None)
        for var in releaseApi.getVariables("${release.id}"):
            if var.key == componentName:
                vp.values = var.value
                listBoxvar = new_variable('Box%s' % componentName, None, vp,'xlrelease.StringVariable',False, componentName,
                                          'List of versions for %s' % componentName)
                releaseApi.createVariable(release.getId(), listBoxvar)


#Add List Box variable to user input task.
#user_input_task = taskApi.searchTasksByTitle(USER_INPUT_TASK_TITLE, phase.title, release.id)[0]
#user_input_task.setVariables(varList)
#Creating a User Input task, adding variables to it from Release variables & then removing the 3rd variable var_hostName.
for componentName in releaseVariables[REPEAT_USING_VARIABLE]:
    for var in releaseApi.getVariables("${release.id}"):
        if var.key == 'Box%s' % componentName:
            varList.append(var)

print len(varList)

print "\n Creating a User Input task B... \n"
phase = getCurrentPhase()
task2 = taskApi.newTask("xlrelease.UserInputTask")
task2.title = "Select Component Versions to Deploy"
task2.setVariables(varList)
taskApi.addTask(phase.id, task2)
