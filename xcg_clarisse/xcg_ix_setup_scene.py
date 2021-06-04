import ix.cmds as cmds

project_name = "Learning Clarisse"

groups_to_create = ['lights','alembic_imp','groups','combiners','scatterers']

for group in groups_to_create:
    cmds.CreateContext(group, "Global", "project://scene")
