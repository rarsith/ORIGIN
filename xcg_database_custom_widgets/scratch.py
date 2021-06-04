branch = list()
category = list()
entry = list()
get_selected_objects = self.project_tree_viewer_wdg.currentItem()

if get_selected_objects is None:
    return []
else:
    try:
        print(get_selected_objects.text(0), "SELECTION")
        print(get_selected_objects.text(0), "entry")
        parent = get_selected_objects.parent()
        print(parent.text(0), 'category')
        grandparent = parent.parent()
        print(grandparent.text(0), "branch")
    except:
        pass

    try:
        if not parent and grandparent:
            branch.append(get_selected_objects.text(0))
            print(get_selected_objects.text(0), "FOLLOW")
    except:
        pass

    try:
        if not grandparent:
            category.append(parent.text(0))
    except:
        pass

    try:
        if parent and grandparent:
            entry.append(get_selected_objects.text(0))
    except:
        pass

print(branch, category, entry)
return branch, category, entry