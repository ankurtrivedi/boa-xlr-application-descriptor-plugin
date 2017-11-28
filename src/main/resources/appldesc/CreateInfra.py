#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Script constants
SUB_RELEASE_TASK_TEMPLATE_TITLE = 'Template task'
GATE_FOR_SUB_RELEASE_DEPENDENCIES_TITLE = 'Wait for Create Infra'
sitInfraList = []


# Cleans the task or variable as if you constructed a new one.
# The 'set$token' method is a tricky one as it's not a valid method name in Python
def clean_persistence_data_of_configuration_item(ci):
    ci.id = None
    getattr(ci, 'set$token')(None)


create_release_task_template = taskApi.searchTasksByTitle(SUB_RELEASE_TASK_TEMPLATE_TITLE, phase.title, release.id)[0]
gate_task = taskApi.searchTasksByTitle(GATE_FOR_SUB_RELEASE_DEPENDENCIES_TITLE, phase.title, release.id)[0]
create_release_tasks_parent_id = create_release_task_template.id[:create_release_task_template.id.rindex('/')]

create_release_task_template_id = create_release_task_template.id
create_release_task_template_newReleaseTitle = create_release_task_template.newReleaseTitle

for var in releaseApi.getVariables("${release.id}"):
    if var.key.startswith("sitinfra"):
        sitInfraList.append(var)

for sitInfra in sitInfraList:
    print sitInfra.key
    generated_task = create_release_task_template
    clean_persistence_data_of_configuration_item(generated_task)
    print len(generated_task.templateVariables)
    clean_persistence_data_of_configuration_item(generated_task.templateVariables[0])
    clean_persistence_data_of_configuration_item(generated_task.templateVariables[1])
    clean_persistence_data_of_configuration_item(generated_task.templateVariables[2])

    # Discover the properties of CreateReleaseTask from docs: https://docs.xebialabs.com/jython-docs/#!/xl-release/6.0.x//service/com.xebialabs.xlrelease.domain.CreateReleaseTask
    generated_task.title = 'Create Infra for ' + sitInfra.key # generated task title
    generated_task.newReleaseTitle = create_release_task_template_newReleaseTitle + sitInfra.key # sub-release title
    sub_release_variable_key = 'subReleaseId_%s' % sitInfra.key
    sub_release_variable_name = '$' + ('{%s}' % sub_release_variable_key) # strange concatenating only to avoid this line from being detected as a new variable in this template
    generated_task.createdReleaseId = sub_release_variable_name # variable to store sub-release ID
    generated_task.templateVariables[0].value = sitInfra.key # sub-release input variable value
    generated_task.templateVariables[1].value = sitInfra.key # sub-release input variable value
    generated_task.templateVariables[2].value = sitInfra.key # sub-release input variable value

    print 'Creating sub-release task "%s" and adding dependency to its release to gate "%s"' % (generated_task.title, gate_task.title)
    taskApi.addTask(create_release_tasks_parent_id, generated_task) # create the task

    taskApi.addDependency(gate_task.id, sub_release_variable_name) # add a dependency to the sub-release via a variable

    # Add the variable to releaseVariables to work around REL-3012
    #releaseVariables[sub_release_variable_key] = ''


taskApi.delete(create_release_task_template_id) # delete the template task as it's done its job
