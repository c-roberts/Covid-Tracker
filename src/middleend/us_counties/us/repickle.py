import os

# re-encode pkl file for windows

original = os.getcwd() + "\\src\\middleend\\us_counties\\us\\states.pkl"
destination = os.getcwd() + "\\src\\middleend\\us_counties\\us\\states.pkl"

content = ''
outsize = 0
with open(original, 'rb') as infile:
    
    content = infile.read()
with open(destination, 'wb') as output:
    
    for line in content.splitlines():
        outsize += len(line) + 1
        output.write(line + str.encode('\n'))

original = os.getcwd() + "\\src\\middleend\\us_counties\\us\\counties.pkl"
destination = os.getcwd() + "\\src\\middleend\\us_counties\\us\\counties.pkl"

content = ''
outsize = 0
with open(original, 'rb') as infile:
    
    content = infile.read()
with open(destination, 'wb') as output:
    
    for line in content.splitlines():
        outsize += len(line) + 1
        output.write(line + str.encode('\n'))