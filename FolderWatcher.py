import hashlib
import os
import time


class FolderWatcher():
    """Class to watch a folder and its subfolder for changes in files with the given extension
    Example of usage:

     def test(*args):
         print(args)

     f = FolderWatcher("C:\\temp")
     files = f.loop_and_check_for_changes_and_deletions_and_additions(test)

    """

    def __init__(self, folder_path, file_extension=""):
        self.folder_path = folder_path
        self.file_extension = file_extension
        self.file_list = self.get_file_list()

    def get_file_list(self):
        """Get a list of all the files in the folder and its subfolders, along with their hashes"""
        file_list = []
        for root, dirs, files in os.walk(self.folder_path):
            for file in files:
                if self.file_extension == "":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as f:
                        content = f.read()
                        hash = hashlib.md5(content).hexdigest()
                        file_list.append((file_path, hash))
                else:
                    if file.endswith(self.file_extension):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'rb') as f:
                            content = f.read()
                            hash = hashlib.md5(content).hexdigest()
                            file_list.append((file_path, hash))
        return file_list

    def check_for_changes(self):
        """Check for files that have been changed on its file contents in the folder and its subfolders."""
        new_file_list = self.get_file_list()
        changed_files = []
        blnNewList = False
        for file in new_file_list:
            if file[0] in [x[0] for x in self.file_list]:
                if file[1] != [x[1] for x in self.file_list if x[0] == file[0]][0]:
                    changed_files.append(file[0])
                    blnNewList = True
        if blnNewList:
            self.file_list = new_file_list
        return changed_files

    def check_for_deletions(self):
        """Check for files that have been deleted in the folder and its subfolders"""
        new_file_list = self.get_file_list()
        deleted_files = []
        blnNewList = False
        for file in self.file_list:
            if file[0] not in [x[0] for x in new_file_list]:
                deleted_files.append(file[0])
                blnNewList = True
        if blnNewList:
            self.file_list = self.get_file_list()
        return deleted_files

    def check_for_changes_and_deletions(self):
        """Check for files that have been changed or deleted in the folder and its subfolders"""
        changes = self.check_for_changes()
        deletions = self.check_for_deletions()
        return changes, deletions

    def check_for_changes_and_deletions_and_additions(self):
        """Check for files that have been added, changed or deleted in the folder and its subfolders"""
        changes, deletions = self.check_for_changes_and_deletions()
        additions = self.check_for_additions()
        return changes, deletions, additions

    def check_for_additions(self):
        """Check for files that have been added in the folder and its subfolders"""
        new_file_list = self.get_file_list()
        added_files = []
        blnNewList = False
        for file in new_file_list:
            if file[0] not in [x[0] for x in self.file_list]:
                added_files.append(file[0])
                blnNewList = True
        if blnNewList:
            self.file_list = new_file_list
        return added_files

    def check_for_changes_and_additions(self):
        """Check for files that have been added or changed in the folder and its subfolders"""
        changes = self.check_for_changes()
        additions = self.check_for_additions()
        return changes, additions

    def check_for_deletions_and_additions(self):
        """Check for files that have been added or deleted in the folder and its subfolders"""
        deletions = self.check_for_deletions()
        additions = self.check_for_additions()
        return deletions, additions

    def loop(self, callback, interval=1):
        """Loop to check for changes in the folder and its subfolders. The callback function is called with the changed files as an argument"""
        while True:
            changed_files = self.check_for_changes()
            if changed_files:
                callback(changed_files)
            time.sleep(interval)

    def loop_and_check_for_deletions(self, callback, interval=1):
        """Loop to check for changes and deletions in the folder and its subfolders. The callback function is called with the changed files and deleted files as arguments"""
        while True:
            changed_files, deleted_files = self.check_for_changes_and_deletions()
            if changed_files or deleted_files:
                callback(changed_files, deleted_files)
            time.sleep(interval)

    def loop_and_check_for_changes_and_deletions_and_additions(self, callback, interval=1):
        """Loop to check for changes and deletions in the folder and its subfolders. The callback function is called with the changed files and deleted files as arguments"""
        while True:
            changed_files, deleted_files, added_files = self.check_for_changes_and_deletions_and_additions()
            if changed_files or deleted_files or added_files:
                callback(changed_files, deleted_files, added_files)
            time.sleep(interval)

    def loop_and_check_for_additions(self, callback, interval=1):
        """Loop to check for additions in the folder and its subfolders. The callback function is called with the added files as an argument"""
        while True:
            added_files = self.check_for_additions()
            if added_files:
                callback(added_files)
            time.sleep(interval)

    def loop_and_check_for_changes_and_additions(self, callback, interval=1):
        """Loop to check for changes and additions in the folder and its subfolders. The callback function is called with the changed files and added files as arguments"""
        while True:
            changed_files, added_files = self.check_for_changes_and_additions()
            if changed_files or added_files:
                callback(changed_files, added_files)
            time.sleep(interval)

    def loop_and_check_for_deletions_and_additions(self, callback, interval=1):
        """Loop to check for deletions and additions in the folder and its subfolders. The callback function is called with the deleted files and added files as arguments"""
        while True:
            deleted_files, added_files = self.check_for_deletions_and_additions()
            if deleted_files or added_files:
                callback(deleted_files, added_files)
            time.sleep(interval)
