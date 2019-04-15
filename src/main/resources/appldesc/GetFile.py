#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

###################################################################################
#  Name: HTTP Get File
#
#  Description: Retrieve the content of file using HTTP GET.
#
#  Known Issues:
###################################################################################

import sys, string, urllib

if server is None:
    print "No server provided."
    sys.exit(1)

#host = { 'url': server }
request = HttpRequest(server, username, password)
response = request.get(uri, contentType=contentType)

if not response.isSuccessful():
    print "Failed to retrieve file from %s/%s" % (server['url'], uri)
    response.errorDump()
    sys.exit(1)
else:
    fileContent = response.getResponse()
    print "Retrieved file content from %s/%s" % (server['url'], uri)
