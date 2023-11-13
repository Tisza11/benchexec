# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0
import re
import benchexec.result as result
import benchexec.tools.template
from benchexec.tools.sv_benchmarks_util import get_data_model_from_task, ILP32, LP64


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for Pi-Violation2Test.
    """

    def executable(self, tool_locator):
        """
        Find the path to the executable file that will get executed.
        @return a string pointing to an executable file
        """
        return tool_locator.find_executable("Violation2Test.sh")

    def version(self, executable):
        return self._version_from_tool(executable)

    def name(self):
        return "pi-violation2test"

    def cmdline(self, executable, options, task, rlimits):
        return (
            [executable]
            + options
            + "--codeFile"
            + list(task.input_files_or_identifier)[0]
            + "--gmlFile"
            + list(task.input_files_or_identifier)[1]
            + "--targetFolder"
            + list(task.input_files_or_identifier)[2]
        )

    def determine_result(self, run):
        status = result.RESULT_UNKNOWN
        for line in run.output:
            if "Aborted ()" in line:
                status = result.RESULT_FALSE_REACH
