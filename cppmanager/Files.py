import pathlib as pl
from pathlib import Path
import datetime as det
import dateutil.tz as tz
import os
import getpass


class Module:
    def __init__(
        self, det, module_suffix, main_suffix
    ):  # det is modulename::namespacename
        assert isinstance(det, str)

        self.namespace = None
        self.class_name = None
        self.module_suffix = module_suffix
        self.main_suffix = main_suffix
        if len(det.split("::")) == 1:
            self.module_name = det.split("::")[0]
        elif len(det.split("::")) == 2:
            self.module_name = det.split("::")[0]
            self.namespace = det.split("::")[1].lower()
        elif len(det.split("::")) == 3:
            self.module_name = det.split("::")[0]
            self.namespace = det.split("::")[1].lower()
            self.class_name = det.split("::")[2].title()

    def deploy(self, path_init):
        ################ HPP ###############

        path = path_init / Path(self.module_name + f".{self.module_suffix}")
        with path.open("w") as f:
            if self.namespace != None:
                id = "_".join(
                    [
                        self.module_name.upper(),
                        self.namespace.upper(),
                        self.module_suffix.upper(),
                    ]
                )
            else:
                id = "_".join([self.module_name.upper(), self.module_suffix.upper()])

            f.write(f"#ifndef {id}\n#define {id}\n\n\n\n")

            if self.namespace != None:
                f.write(f"namespace {self.namespace}\n@\n    \n".replace("@", "{"))

                if self.class_name != None:
                    f.write(
                        f"    class {self.class_name}\n    @\n        public:\n\n        private:\n\n".replace(
                            "@", "{"
                        )
                    )
                    f.write(f"    @; // class {self.class_name}\n\n".replace("@", "}"))
                f.write(f"@ // namespace {self.namespace}\n\n\n".replace("@", "}"))
            f.write(f"#endif // {id}")

        ################ CPP ###############
        path = path_init / Path(self.module_name + f".{self.main_suffix}")
        with path.open("w") as f:
            f.write(f'#include "{self.module_name}.{self.module_suffix}"\n')

            if self.namespace != None:
                f.write(f"namespace {self.namespace}\n@\n    \n".replace("@", "{"))
                f.write(f"@ // namespace {self.namespace}\n\n\n".replace("@", "}"))

    def get_header_include(self):
        return f'#include "{self.module_name}.{self.module_suffix}"'


class Main_File:
    def __init__(self, det, main_suffix, header_suffix):
        assert type(det) is str
        self.main_suffix = main_suffix
        self.header_suffix = header_suffix
        self._name = det + f".{self.main_suffix}"
        self.headers_includes = []

    def add_header_include(self, include):
        assert type(include) is str
        assert include.startswith("#include ")
        self.headers_includes.append(include)

    def deploy_at_init(self, PATH):

        time = det.datetime.now(tz.tzlocal())
        path = PATH / Path(self._name)
        with path.open("w") as f:
            f.write(f"// File : {self._name}\n")

            f.write(
                "// Created : "
                + time.strftime("%A %d %B")
                + " at "
                + time.strftime("%H")
                + "h - "
                + time.strftime("%M")
                + "min\n"
            )
            f.write(f"// user : {getpass.getuser()}")
            f.write(f"\n\n//// PERSONAL MODULES\n")

            if len(self.headers_includes) != 0:
                for include in self.headers_includes:
                    f.write(f"{include}\n")
            f.write(
                "\n\n\n//// BUILTIN LIBS\n#include <iostream>\n\n\n\nint main(){\n\n     return 0;\n}\n"
            )

    def deploy_at_runtime(self, PATH):
        path = PATH / Path(self._name)
        raw_data = None
        with path.open("r") as f:
            raw_data = f.read()
        sep = "//// PERSONAL MODULES\n"
        if sep in raw_data:
            raw_data_splited = raw_data.split(sep)
            start, end = raw_data_splited[0], raw_data_splited[1]
            new_includes = str()
            for include in self.headers_includes:
                new_includes += include + "\n"
            new_raw_data = start + sep + new_includes + end
            with path.open("w") as f:
                f.write(new_raw_data)
        else:
            for include in self.headers_includes:
                new_includes += include + "\n"
            with path.open("w") as f:

                f.write(new_includes + raw_data)

    def exists(self, PATH):
        return self.get_path(PATH).exists()

    def get_path(self, PATH):
        return PATH / Path(self._name)
