#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016 Stefano Maggiolo <s.maggiolo@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""C-like + GCC-like programming language definitions."""

from cms.grading import CompiledLanguage

def make_clike(compiler, lang, std, source_extensions, header_extensions):
    class CLikeLanguageGccLikeCompiler(CompiledLanguage):
        @property
        def name(self):
            return f"{lang.capitalize()}{std} / {compiler}"

        @property
        def source_extensions(self):
            return source_extensions

        @property
        def header_extensions(self):
            return header_extensions

        @property
        def object_extensions(self):
            return [".o"]

        def get_compilation_commands(self,
                                    source_filenames, executable_filename,
                                    for_evaluation=True):
            command = [f"/usr/bin/{compiler}"]
            if for_evaluation:
                command += ["-DEVAL"]
            command += [f"-std={lang}{std}", f"-x{lang}", "-O2", "-pipe", "-static",
                        "-s", "-o", executable_filename]
            command += source_filenames
            command += ["-lm"]
            return [command]

    return CLikeLanguageGccLikeCompiler

CPP_SOURCE_EXTENSIONS = [".cpp", ".cc", ".cxx", ".c++", ".C"]
CPP_HEADER_EXTENSIONS = [".h", ".hpp"]

C_SOURCE_EXTENSIONS = [".c"]
C_HEADER_EXTENSIONS = [".h"]

def make_cpp(compiler, std):
    return make_clike(compiler, "c++", std, CPP_SOURCE_EXTENSIONS, CPP_HEADER_EXTENSIONS)

def make_c(compiler, std):
    return make_clike(compiler, "c", std, C_SOURCE_EXTENSIONS, C_HEADER_EXTENSIONS)

Cpp11Gpp = make_cpp("g++", "11")
Cpp14Gpp = make_cpp("g++", "14")
Cpp17Gpp = make_cpp("g++", "17")
Cpp20Gpp = make_cpp("g++", "20")
Cpp23Gpp = make_cpp("g++", "23")
Cpp26Gpp = make_cpp("g++", "26")

C11Gcc = make_c("gcc", "11")
C23Gcc = make_c("gcc", "23")

__all__ = [
    "Cpp11Gpp",
    "Cpp14Gpp",
    "Cpp17Gpp",
    "Cpp20Gpp",
    "Cpp23Gpp",
    "Cpp26Gpp",
    "C11Gcc",
    "C23Gcc",
]
