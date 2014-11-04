###############################################################################
##     dataextractor module extracts the data from a FDL binary file.
##
##     Copyright (C) 2013  MAX IV Laboratory, Lund Sweden.
##
##     This program is free software: you can redistribute it and/or modify
##     it under the terms of the GNU General Public License as published by
##     the Free Software Foundation, either version 3 of the License, or
##     (at your option) any later version.
##
##     This program is distributed in the hope that it will be useful,
##     but WITHOUT ANY WARRANTY; without even the implied warranty of
##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##     GNU General Public License for more details.
##
##     You should have received a copy of the GNU General Public License
##     along with this program.  If not, see [http://www.gnu.org/licenses/].
###############################################################################

__author__ = 'antmil'

import numpy as np

# filename = 'data/Diags20140702162255 - default.dat'
#
# fd = open(filename, 'rb')
# line = fd.read()
# size = len(line) / 2
# print size
# read_values = np.ndarray(buffer=line, shape=(1, size), dtype=np.int16)
# print read_values
# print len(read_values)
# print read_values[0]
# print np.where(read_values == 32767)[1]


class FDLDataExtractor():
    """ for FDL diag
        Read 16 positions
        Find the comma
        Extract signals A&B
        Transform to values
        Save signals in vectors
    """

    COMA = 32767
    CAV_A = 1
    CAV_B = 2

    def __init__(self, filename):
        #with open(filename, 'rb') as fd:
        #    self.read_values = np.fromfile(fd, dtype='<h,<h')

        with open(filename, 'rb') as fd:
            self._read_values = np.fromfile(fd, dtype='<h')
            #self.read_values.reshape(len(self.read_values)/2,2)
            self._values_a = self._read_values[::2]
            self._values_b = self._read_values[1::2]

        #self._iterator = np.nditer(self._read_values, flags=['multi_index'])
        self._iterator_a = np.nditer(self._values_a)
        self._iterator_b = np.nditer(self._values_b)

    def run(self):
        self.find_next_comma(self._iterator_a)
        self.find_next_comma(self._iterator_b)
    
    def find_next_comma(self, iterator):
        """This method will search for the next comma in the data and will
            return the index value where its found.
        """
        while not iterator.value == self.COMA:
            #print "index: %d, value: %d" %(iterator.iterindex, iterator.value)
            #print "indexmulti: %s" %(self._iterator_a.multi_index)
            iterator.next()
        return iterator.iterindex
    
    def get_indexes(self):
        indexes = np.where(self.read_values == self.comma)[1]
        return indexes

    def clear_pre_data(self):
        self.reduced_values = self.read_values[0, self.comma_indexes[0]:]
