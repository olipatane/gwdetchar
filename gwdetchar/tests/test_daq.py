# -*- coding: utf-8 -*-
# Copyright (C) Joshua Smith (2016-)
#
# This file is part of the GW DetChar python package.
#
# gwdetchar is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# gwdetchar is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gwdetchar.  If not, see <http://www.gnu.org/licenses/>.

"""Tests for :mod:`gwdetchar.daq`
"""

import pytest

import numpy
from numpy.testing import assert_array_equal

from gwpy.segments import (Segment, SegmentList)
from gwpy.timeseries import TimeSeries
from gwpy.tests.utils import assert_segmentlist_equal

from .. import daq


OVERFLOW_SERIES = TimeSeries([0, 0, 0, 1, 1, 0, 0, 1, 0, 1], dx=.5)
CUMULATIVE_SERIES = TimeSeries([0, 0, 0, 1, 2, 2, 2, 3, 3, 4], dx=.5)
OVERFLOW_TIMES = numpy.array([1.5, 3.5, 4.5])
OVERFLOW_SEGMENTS = SegmentList([
    Segment(1.5, 2.5),
    Segment(3.5, 4),
    Segment(4.5, 5),
])


@pytest.mark.parametrize('cmltv, series', [
    (False, OVERFLOW_SERIES),
    (True, CUMULATIVE_SERIES),
])
def test_find_overflows_and_segments(cmltv, series):
    times = daq.find_overflows(series, cumulative=cmltv)
    assert_array_equal(times, OVERFLOW_TIMES)

    segments = daq.find_overflow_segments(series, cumulative=cmltv)
    assert_segmentlist_equal(segments.active, OVERFLOW_SEGMENTS)


def test_ligo_accum_overflow_channel():
    assert daq.ligo_accum_overflow_channel(4, ifo='X1') == (
        'X1:FEC-4_ACCUM_OVERFLOW')
