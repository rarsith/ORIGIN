import os

try:
    xchange_root =  os.environ["XCHANGE_ROOT"]
except:
    print "XCHANGE_ROOT environment variable not correctly configured"

else:
    import sys
    print (xchange_root)
    if not xchange_root in sys.path:
        sys.path.append(xchange_root)


os.environ['XCG_PROJECT']='Test'
os.environ['XCG_PROJECT_BRANCH']='sequences'
os.environ['XCG_PROJECT_CATEGORY']='TST'
os.environ['XCG_PROJECT_ENTITY']= '0100'
os.environ['XCG_ENTITY_TASK']='animation'