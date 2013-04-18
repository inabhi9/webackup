import string, os, random, re

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def ext_file(file_name):
    h, t = os.path.split(file_name)
    try:
        return '.'+t.split('.', 1)[1]
    except IndexError:
        return ''
    
def clean_str(s):
    s = s.lower()
    pattern = "[\W]+"
    s = re.sub(pattern, "-", s)
    s = re.sub("[\W]$", "", s)
    return s