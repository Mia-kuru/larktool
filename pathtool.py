# -*-python 3.10-*-
import os as os
import sys as _sys
import shutil
import re
import inspect
import zipfile

from .utils import encoding

import warnings
__all__ = ["is_exist", "is_dir", "is_file", "enable_dir", "mkdir"
           , "get_cwd", "SimplePath", "WorkSpace"
           , "current_func_running_file_dir"]

TABLE_STR = {
    0:'├',
    1:'└',
    2:'─',
    3:'|'
}

def is_exist(path) -> bool:
    """Check whether the file exists."""
    return os.path.exists(path)


def is_dir(path) -> bool:
    """Check whether paht is dir"""
    return os.path.isdir(path)


def is_file(path) -> bool:
    """Check whether paht is file"""
    return os.path.isfile(path)


def enable_dir(filename:str) -> str:
    """Check path dir whether exists.
    if not path dir, it will create dir. And return the filename.
    """
    folder = os.path.dirname(filename)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return filename


def mkdir(path:str):
    """make dir, defulat mode = 777"""
    os.makedirs(path, exist_ok=True)


def get_cwd():
    """Return cwd"""
    return os.getcwd()


def current_func_running_file_dir():
    """Defualt return the function runing py file's dir, 
    Returns the path to the file from which the function was called
    """
    frame = inspect.currentframe()
    caller_file = inspect.getfile(frame.f_back)

    curdir = os.path.dirname(os.path.abspath(caller_file))
    return curdir


def chdir(base=None):
    """base is None, path where"""
    cwd = base or "."
    os.chdir(cwd)


class DefinedStr(str):
    def __new__(cls, value=""):
        return super(DefinedStr, cls).__new__(cls, value)

class DirTree:
    def __init__(self, files=None, dirs=None):
        self.default_tree = dict()
        self.default_tree.setdefault("file", [])
        self.default_tree.setdefault("dir", [])
        # return tuple("parent_name", tree:dict)

    def get_file(self):
        pass

class DeletDirTreeWarning(Warning):
    """dir tree cannot be deleted implicitly"""


class SimplePath(DefinedStr):
    """Path class.
    """
    def __init__(self, root="") -> None:
        if '/' in root:
            self.join_str = '/'
        else:
            self.join_str = '\\'

        self.path_value = self.__format(root)

    def i(self, path_name):
        """Insert path, 
        self.ixxx == self.i('xxx') equal insert xxx dir.
        
        Args:
            path_name (str): folder or file name.
        """
        path_name = self.__format(path_name)
        new_path = self.__add_path(path_name)

        return SimplePath(new_path)

    def mk(self, folder):
        """Make dir"""
        folder = self.__format(folder)
        new_path = self.__add_path(folder)

        if not is_exist(new_path):
            mkdir(new_path)

        return SimplePath(new_path)

    def add(self, folder):
        """Add dir, if dir not exist, func will create it."""
        return self.mk(folder)

    def cd(self, path):
        path = self.__format(path)

        if path.split(self.join_str)[0] in [".", ".."]:
            path = self.__add_path(path)

        new_path = os.path.normpath(path)
        return SimplePath(new_path)

    def back(self, n=1):
        """Back to `n` layer parent dir."""
        new_path = self.path_value.rsplit(self.join_str, n)[0]

        return SimplePath(new_path)

    def remove(self, *, rmtree=False) -> bool:
        """Remove file or dir."""
        # TODO: 限制删除目录的范围
        if not self.is_exist:
            return False
        if self.is_dir:
            try:
                os.rmdir(self.path_value)
            except OSError:
                if rmtree is False:
                    warnings.warn("You are deleting a dir tree. "
                                "It cannot be deleted implicitly. "
                                "Please set rmtree is `True`", 
                                DeletDirTreeWarning)
                    return False
                shutil.rmtree(self.path_value)
        else:
            os.remove(self.path_value)
        return True

    rm = remove

    def move(self, dst_path) -> bool:
        """Move file or dir to dst"""
        try:
            # HACK:
            # print('"%s" move to "%s"' % (self.path_value, dst_path))
            shutil.move(self.path_value, dst_path)
            return True
        except FileExistsError:
            warnings.warn("%s FileExists!" % dst_path
                          , RuntimeWarning)
            return False

    def copy(self, dst_path):
        """Copy file or dir to dst"""
        if is_dir(self.path_value):
            shutil.copytree(self.path_value, dst_path)
        if is_file(self.path_value):
            shutil.copy(self.path_value, dst_path)

    def tree(self):
        # TODO: 输出文件结构树，返回字典
        pass

    def ls(self, out="all", search=None):
        """Return current dir's list"""
        # HACK: 
        items = os.listdir(self.path_value)

        if out == "file":
            items = [item for item in items if is_file(self.__add_path(item))]
        elif out in ["dir", "folder"]:
            items = [item for item in items if is_dir(self.__add_path(item))]

        if search:
            pattern = re.compile(search)
            items = [item for item in items if pattern.search(item)]

        return items

    def lsfile(self, search=None):
        return self.ls(out='file', search=search)

    def lsdir(self, search=None):
        return self.ls(out='dir', search=search)

    def lstree(self):
        pass

    def escape(self):
        """Return all escape path"""
        return re.escape(self.path_value)

    def cp(self):
        """Copy path, and return SimplePath"""
        return SimplePath(self.path_value)

    def to_zip(self, pwd=None):
        # TODO: 设置密码
        try:
            zipf = zipfile.ZipFile(self.dot("zip"), 'w'
                                   , zipfile.ZIP_DEFLATED)
            if self.is_file:
                zipf.write(self.path_value, self._base_name())
            elif self.is_dir:
                for item in self.ls():
                    zipf.write(self.__add_path(item), item)
        finally:
            zipf.close()

    def ext_zip(self):
        # TODO: 解压
        pass

    def mkfile(self, file_name:str):
        """Make file"""
        # HACK:
        try:
            if self.is_file:
                parent = self._parent()
                path = self.__merge_path(parent, file_name)
            else:
                path = self.__add_path(file_name)
            if is_exist(path):
                file = None
                return
            file = open(path, 'w', encoding="utf-8")
        finally:
            if file is not None:
                file.close()

    def openfile(self,
            mode="r", 
            encoding=encoding.UTF8, 
            newline=None
            ):
        # HACK:
        return open(self.path_value
                    , mode=mode
                    , encoding=encoding
                    , newline=newline
               )

    def crate_file(self):
        self.mkfile(self._base_name())

    def crate_dir(self):
        enable_dir(self.path_value)

    def file_type(self, to_type_name=None):
        """Get file type, 
        if set to_type_name, file type will become it.

        Args:
            to_type_name (str): Change to type_name suffix.
                if it is `None` func will return type_name, 
                or else return changed filename suffix path.
        
        Returns:
            str|SimplePath: 
            to_type_name is `None` return `str`, or else `SimplePath`.
            if path is folder. return `""`.
        """
        if to_type_name is None and self.is_dir:
            warnings.warn("%s folder is not file type." % self.path_value,
                          Warning)
            return ""

        file_name = self._base_name()
        parent = self._parent()

        if "." not in file_name:
            file_name = file_name + "."

        name, type_name = file_name.rsplit('.', 1)

        if to_type_name is not None:
            new_file_name = name + "." + to_type_name
            new_path = self.__merge_path(parent, new_file_name)
            return SimplePath(new_path)

        return type_name
    
    def dot(self, suffix=None):
        """Set path, add dot and suffix.
        
        if suffix is None, don't set path.
        """
        if suffix is None:
            suffix = ''
        return SimplePath(self.path_value + ".{}".format(suffix))

    def __format(self, value:str) -> str:
        value = value.strip(" \n\t")
        return re.sub("[\\\\/]", re.escape(self.join_str), value)

    def __merge_path(self, parent:str, value:str) -> str:
        return self.join_str.join((parent, value.lstrip("\\/")))

    def __add_path(self, value:str) -> str:
        return self.__merge_path(self.path_value, value)

    def _parent(self) -> str:
        """Return self.path_value's parent."""
        return os.path.dirname(self.path_value)

    def _base_name(self):
        """Return self.path_value's base_name(file or dir name)."""
        return os.path.basename(self.path_value)

    def __add__(self, value):
        return SimplePath(self.path_value + self.__format(value))

    def __getattr__(self, name):
        if name[0] == 'i':
            # self.ixxx  -> self.i('xxx')
            return self.i(name[1:])
        elif "dot_" in name and name.startswith("dot_"):
            # self.dot_py  -> self.dot('py')
            return self.dot(name[4:])
        else:
            # Default get attribute
            return object.__getattribute__(self, name)

    @property
    def is_file(self):
        return is_file(self.path_value)

    @property
    def is_dir(self):
        return is_dir(self.path_value)

    @property
    def is_exist(self):
        return is_exist(self.path_value)


class WorkSpace:
    def __init__(self, work_space_list:list=["."]) -> None:
        self.work_list_dict = dict()

        if not isinstance(work_space_list, list):
            raise TypeError("work_space_list type must be list")

        for i, work_path in enumerate(work_space_list):
            self.work_list_dict[i+1] = work_path
        else:
            self.max_idx = i+1

        self.using_workspace = self.work_list_dict[1]

    def using_workdir(self, num=1):
        """get work space, you can self.w1 => num = 1"""
        work_path = self.work_list_dict.get(num, self.using_workspace)
        self.using_workspace = work_path
        return SimplePath(work_path)

    def add_workdir(self, work_path):
        """add into work_list_dict"""
        if len(self.work_list_dict.keys()) > 30:
            return
        self.max_idx += 1
        self.work_list_dict[self.max_idx] = work_path

    def to_list(self):
        return self.work_list_dict.values()

    def built_dirs(self):
        for workdir in self.to_list():
            enable_dir(workdir)
        return self

    def __getattr__(self, name) -> SimplePath:
        if name[0] == "w" and name[1:].isdigit():
            # self.w1 -> self.using_workdir(1)
            return self.using_workdir(int(name[1:]))
        else:
            # try SimlePath's method
            return getattr(SimplePath(self.using_workspace), name)

    def __getitem__(self, item):
        if isinstance(item, int):
            raise TypeError("item must be int")
        return self.using_workdir(item)


def format_size(size_in_bytes, unit="b", to_unit="gb"):
    # FIXME: 不符合预期
    SIZE_UNIT = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = SIZE_UNIT.index(unit.upper())
    to_unit_index = SIZE_UNIT.index(to_unit.upper())

    if unit_index > to_unit_index:
        raise ValueError("from_unit must be smaller than to_unit")

    for unit in SIZE_UNIT:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024