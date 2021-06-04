import maya.cmds as cmds

def get_outliner():
    outliner_content = cmds.ls (typ='transform')
    return outliner_content
    
def create_entry_attr(object_name, attr_name, attr_value, lock_attrib=True):
    try:
        cmds.addAttr(ln=attr_name, dt="string")
        attribute_capture = str(object_name +'.'+ attr_name)
        cmds.setAttr(attribute_capture, attr_value, typ='string', l=lock_attrib)
    except:
        print ("Attribute >> {0} = {1}, already exists, bypassing!".format(attr_name, attr_value))