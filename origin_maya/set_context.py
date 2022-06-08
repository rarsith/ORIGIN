import os

try:
    origin_root =  os.environ["ORIGIN_ROOT"]
except:
    print ("ORIGIN_ROOT environment variable not correctly configured")

else:
    import sys
    print (origin_root)
    if not origin_root in sys.path:
        sys.path.append(origin_root)


os.environ['ORIGIN_PROJECT']='Remus'
os.environ['ORIGIN_PROJECT_BRANCH']='assets'
os.environ['ORIGIN_PROJECT_CATEGORY']='characters'
os.environ['ORIGIN_PROJECT_ENTITY']= 'donkey'
os.environ['ORIGIN_ENTITY_TASK']='modeling'