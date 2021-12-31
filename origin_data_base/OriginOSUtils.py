from origin_data_base.OriginUsers import OriginUsers
from origin_data_base.OriginEnvar import OriginEnvar

class OriginOSUtils(object):


    def create_path(self, elements_list):
        import os
        return os.path.join(*elements_list)

    @staticmethod
    def base_save_path():
        proj_root = oenv.get_project()
        branch = oenv.get_branch()
        category = oenv.get_category()
        entity = oenv.get_entity()
        task = oenv.get_task()
        return os.path.join(proj_root, branch, category, entity, task)


    @staticmethod
    def next_file_version(folder_path):
        import os
        import re
        all_files = list()
        get_files = os.listdir(folder_path)
        if not len(get_files)<1:
            for dirs in get_files:
                all_files.append(dirs)
            print (all_files)
            highest = max(all_files)
            get_digit = filter(None, re.split(r'(\d+)', highest))
            get_digit_list = (list(get_digit))

            return  "{0}{1:04d}".format(("v"),(int(get_digit_list[1])+1))
        else:
            return "{0}{1:04d}".format(("v"),(int(1)))

    @staticmethod
    def wip_output_path():
        users = "users"
        who = OriginUsers.get_curr_user()
        saving_path = save_path()
        path_to_output = os.path.join(saving_path, users, who,'')
        if not os.path.exists(path_to_output):
            os.makedirs(path_to_output)
        return path_to_output


if __name__ == "__main__":
 pass

