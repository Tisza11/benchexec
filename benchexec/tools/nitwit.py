# This file is part of BenchExec, a framework for reliable benchmarking:
# https://github.com/sosy-lab/benchexec
#
# SPDX-FileCopyrightText: 2007-2020 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import logging
import os

import benchexec.result as result
import benchexec.tools.template


class Tool(benchexec.tools.template.BaseTool2):
    """
    Tool info for the NITWIT Validator, an interpreter-based violation witness validator.
    URL: https://github.com/moves-rwth/nitwit-validator
    """

    REQUIRED_PATHS = []
    BIN_DIR = "bin"

    def executable(self, tool_locator):
        executable = tool_locator.find_executable("nitwit.sh")
        bin_path = os.path.join(os.path.dirname(executable), self.BIN_DIR)
        if (
            not os.path.isdir(bin_path)
            or not os.path.isfile(os.path.join(bin_path, "nitwit32"))
            or not os.path.isfile(os.path.join(bin_path, "nitwit64"))
        ):
            logging.warning(
                "Required binary files for Nitwit not found in {0}.".format(bin_path)
            )
        return executable

    def program_files(self, executable):
        return [
            executable,
            os.path.join(self.BIN_DIR, "nitwit32"),
            os.path.join(self.BIN_DIR, "nitwit64"),
        ]

    def version(self, executable):
        return self._version_from_tool(executable, "--version")

    def name(self):
        return "Nitwit"

    def cmdline(self, executable, options, task, rlimits):
        if task.property_file:
            options = options + ["-p", task.property_file]
        return [executable] + options + task.single_input_file

    def determine_result(self, run):
        """
        See README.md at https://github.com/moves-rwth/nitwit-validator for information
        about result codes.
        @return: status of validator after executing a run
        """
        if run.exit_code.signal is None and (run.exit_code.value == 0 or run.exit_code.value == 245):
            status = result.RESULT_FALSE_REACH
        elif run.exit_code.value is None or run.exit_code.value in [-9, 9]:
            status = "TIMEOUT"
        elif run.exit_code.value in [4, 5, 241, 242, 243, 250]:
            status = result.RESULT_UNKNOWN
        else:
            status = result.RESULT_ERROR

        if run.output.any_line_contains("Out of memory") or (run.exit_code.value == 251):
            status = "OUT OF MEMORY"

        if not status:
            status = result.RESULT_ERROR

        return status
