#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2016-2017 Stefano Maggiolo <s.maggiolo@gmail.com>
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

"""C# programming language definition, using the .NET framework.
"""

from cms.grading import Language


__all__ = ["CSharpDotNET"]


class CSharpDotNET(Language):
    """This defines the C# programming language, compiled and executed
    with the cross-platform .NET framework.
    """

    @property
    def name(self):
        """See Language.name."""
        return "C# / .NET"

    @property
    def source_extensions(self):
        """See Language.source_extensions."""
        return [".cs"]

    @property
    def executable_extension(self):
        """See Language.executable_extension."""
        return ".zip"

    @property
    def requires_multithreading(self):
        """See Language.requires_multithreading."""
        return True

    def get_compilation_commands(self,
                                 source_filenames, executable_filename,
                                 for_evaluation=True):
        """See Language.get_compilation_commands."""
        return [
            ["/usr/bin/env", "DOTNET_SKIP_WORKLOAD_INTEGRITY_CHECK=1", "DOTNET_NOLOGO=1",
                "/usr/bin/dotnet", "new", "console", "--verbosity=quiet", "--name=submission"],
            ["/usr/bin/rm", "submission/Program.cs"],
            ["/usr/bin/cp"] + source_filenames + ["submission/"],
            ["/usr/bin/dotnet", "restore", "submission", "--verbosity=quiet", "--source=/opt/dotnet-packages"],
            ["/usr/bin/dotnet", "publish", "submission", "--verbosity=quiet", "--no-restore", "--configuration=Release", "--output=final"]
                + (["/p:DefineConstants=EVAL"] if for_evaluation else []),
            ["/usr/bin/zip", "-r", executable_filename, "final/"],
        ]

    def get_evaluation_commands(
            self, executable_filename, main=None, args=None):
        """See Language.get_evaluation_commands."""
        return [
            ["/usr/bin/unzip", executable_filename],
            ["/usr/bin/env", "DOTNET_EnableWriteXorExecute=0",
                "/usr/bin/dotnet", "final/submission.dll"],
        ]

"""
#!/bin/sh

# C# compile wrapper-script for 'compile.sh'.
# See that script for syntax and more info.
#
#
# This script requires dotnet-sdk to be installed in the chroot.
set -e

DEST="$1" ; shift
MEMLIMIT="$1" ; shift
MAINSOURCE="$1"

SOURCEDIR="${MAINSOURCE%/*}"
[ "$SOURCEDIR" = "$MAINSOURCE" ] && SOURCEDIR='.'

WORKDIR=$(mktemp -d "./tmp.XXXXXXXXXX")
trap 'rm -rf "$WORKDIR"' EXIT

PROJDIR="$WORKDIR/project"
mkdir -p "$PROJDIR"

cat > "$PROJDIR/$DEST.csproj" <<EOF
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>
    <DefineConstants>ONLINE_JUDGE</DefineConstants>
  </PropertyGroup>
</Project>
EOF

cp -r "$@" "$PROJDIR"

mkdir -p "$WORKDIR/tmp"
mkdir -p "$WORKDIR/home"
mkdir -p "$WORKDIR/data"
mkdir -p "$WORKDIR/cli-home"

env -i \
    TMPDIR="$WORKDIR/tmp" \
    HOME="$WORKDIR/home" \
    XDG_DATA_HOME="$WORKDIR/data" \
    DOTNET_NOLOGO=1 \
    DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_CLI_HOME="$WORKDIR/cli-home" \
    DOTNET_EnableWriteXorExecute=0 \
    dotnet publish "$PROJDIR" -o .

mv "$DEST" "$DEST.exe"

cat > "$DEST" <<EOF
#!/bin/sh

# Detect dirname and change dir to prevent class not found errors.
if [ "\${0%/*}" != "\$0" ]; then
    cd "\${0%/*}"
fi

export DOTNET_EnableWriteXorExecute=0
exec "./$DEST.exe"
EOF

chmod a+x "$DEST"

exit 0
"""
