#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import sys, string, time
import com.xhaus.jyson.JysonCodec as json
from com.xebialabs.xlrelease.domain import Task
from com.xebialabs.deployit.plugin.api.reflect import Type
from java.text import SimpleDateFormat
from com.xebialabs.xlrelease.api.v1.forms import Variable


# Script constants
GROUP_TASK_TITLE = 'Components Tasks'
REPEAT_USING_VARIABLE = 'ComponentList'
USER_INPUT_TASK_TITLE = 'Gate Task'


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

def createScriptBasedTask(phaseId,taskTypeValue,title,precondition, propertyMap):
    parenttaskType = Type.valueOf("xlrelease.CustomScriptTask")

    parentTask = parenttaskType.descriptor.newInstance("nonamerequired")
    parentTask.setTitle(title)

    childTaskType = Type.valueOf(taskTypeValue)
    childTask = childTaskType.descriptor.newInstance("nonamerequired")
    for item in propertyMap:
        childTask.setProperty(item,propertyMap[item])
    parentTask.setPythonScript(childTask)
    parentTask.setPrecondition(precondition)

    taskApi.addTask(phaseId,parentTask)

group_task_id = taskApi.searchTasksByTitle(GROUP_TASK_TITLE, phase.title, release.id)[0].id
user_input_task = taskApi.searchTasksByTitle(USER_INPUT_TASK_TITLE, phase.title, release.id)[0]

for componentName in releaseVariables[REPEAT_USING_VARIABLE]:
    print componentName
    print group_task_id

    #Create a list variable to get all versions.
    listvar = new_variable(componentName, None, None,
                           'xlrelease.ListStringVariable',
                           False, componentName,
                           'List of versions for %s' % componentName)
    releaseApi.createVariable(release.getId(), listvar)

    createScriptBasedTask(group_task_id,"xldeploy.GetAllVersionsTask", "Get All Version for %s" %componentName ,None,{"applicationId":componentName, "throwOnFail":False, "username": "", "password":"","packageIds":"componentName"})


#Add Output Variable
for task in releaseApi.getActiveTasks("${release.id}"):
    if task.title == "Get All Version for %s" %componentName:
        vp.values = var.value
