#!/usr/bin/env python3

# Contest Management System - http://cms-dev.github.io/
# Copyright © 2010-2012 Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
# Copyright © 2010-2018 Stefano Maggiolo <s.maggiolo@gmail.com>
# Copyright © 2010-2012 Matteo Boscariol <boscarim@hotmail.com>
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

import re
from . import ScoreTypeGroup


class GroupSum(ScoreTypeGroup):
    """The score of a submission is the sum of the product of the
    average of the ranges with the multiplier of that range.

    Parameters are [[m, t], ... ] (see ScoreTypeGroup).

    """

    def get_group_testcase_count(self, t_param):
        """Return the number of testcases in the current group.
        
        t_param: the second parameter of the group (see ScoreTypeGroup)
        
        """
        
        if isinstance(t_param, int):
            return t_param
        
        elif isinstance(t_param, str):
            indices = self.public_testcases.keys()
            regexp = re.compile(t_param)
            cases = [tc for tc in indices if regexp.match(tc)]
            if not cases:
                raise ValueError(
                    f"No testcase matches against the regexp '{t_param}'")
            return len(cases)
        
        raise ValueError(
            "In the score type parameters, the second value "
            "must have the type int or str")

    def get_public_outcome(self, outcome, parameter):
        """See ScoreTypeGroup."""
        
        group_tc_count = self.get_group_testcase_count(parameter[1])
        tc_score = parameter[0] / group_tc_count
        
        return f"{outcome * tc_score :g} / {tc_score :g}"

    def reduce(self, outcomes, unused_parameter):
        """See ScoreTypeGroup."""
        
        return sum(outcomes) / len(outcomes)
