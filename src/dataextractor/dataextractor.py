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
    NUM_OF_SIGNALS = 15
    SIGNALS = ['IrvTet1',
               'QrvTet1',
               'IrvTet2',
               'QrvTet2',
               'IFwCirc',
               'QFwCirc',
               'IrvCirc',
               'QrvCirc',
               'IFwLoad',
               'QFwLoad',
               'IFwHybLoad',
               'QFwHybLoad',
               'IrvCav',
               'QrvCav',
               'AmpMO']

    def __init__(self, filename):
        #with open(filename, 'rb') as fd:
        #    self.read_values = np.fromfile(fd, dtype='<h,<h')

        with open(filename, 'rb') as fd:
            self._read_values = np.fromfile(fd, dtype='<h')
            #self.read_values.reshape(len(self.read_values)/2,2)
            self._values_a = self._read_values[::2]
            self._values_b = self._read_values[1::2]

        #self._iterator = np.nditer(self._read_values, flags=['multi_index'])
        self._iterator_a = np.nditer(self._values_a, flags=['f_index'])
        self._iterator_b = np.nditer(self._values_b, flags=['f_index'])

        #initialise dict of signals
        self._raw_signals = { self.CAV_A: {},
                              self.CAV_B: {}
                            }
        self._signals = {
                            self.CAV_A: {},
                            self.CAV_B: {},
                        }
        
        for signal in self.SIGNALS:
            self._raw_signals[self.CAV_A][signal] = []
            self._raw_signals[self.CAV_B][signal] = []

    def extract_raw_values(self, iterator, cavity):
        while not iterator.finished:
            index = self.find_next_comma(iterator)
            self.add_values_from_index(index, cavity)

    def extract_values(self):
        for cavity in [self.CAV_A, self.CAV_B]:
            if cavity == self.CAV_A:
                iterator = self._iterator_a
            else:
                iterator = self._iterator_b

            while not iterator.finished:
                index = self.find_next_comma(iterator)
                self.add_values_from_index(index, cavity)
        
        self.convert_all_values_to_mv()
    
    def find_next_comma(self, iterator):
        """This method will search for the next comma in the data and will
            return the index value where its found.
        """
        # if not iterator.finished:
        #     if iterator.value == self.COMA:
        # iterator.iternext()
        # if not iterator.finished:
        #     while not iterator.value == self.COMA:
        # # while not iterator[0] == self.COMA:
        #         if not iterator.finished:
        #             iterator.iternext()
        #         else:
        #             break
        #     # return iterator.iterindex
        # return iterator.index

        while not iterator.finished:
            if iterator.value == self.COMA:
                index = iterator.index
                iterator.iternext()
                return index
            else:
                iterator.iternext()
        #return iterator.index

    def add_values_from_index(self, index, cavity):
        """ Add all the signals values starting from an index.
        """
        if cavity == self.CAV_A:
            values = self._values_a
        elif cavity == self.CAV_B:
            values = self._values_b
        else:
            raise "Wrong CAVITY!"

        try:
            if index is not None:
                if self.acquisition_has_enough_values(values, index):
                    for i,signal in enumerate(self.SIGNALS):
                        self._raw_signals[cavity][signal].append(values[index+i+1])
        except:
            raise

        #for signal in self.SIGNALS:
        #    print 'Signal: %s, Value: %d' %(signal, self._raw_signals[cavity][signal])
        #print self._values_a

    def acquisition_has_enough_values(self, values, index):
        try:
            val = values[index + self.NUM_OF_SIGNALS]
            return True
        except IndexError:
            return False
        except:
            raise


    def get_raw_value(self, signal, cavity, index):
        """Method to return the list of values of one single signal.
        """
        return self._raw_signals[cavity][signal][index]

    def get_value(self, signal, cavity, index):
        """Returns the value converted to the correct units.
        """
        value = self._raw_signals[cavity][signal][index]
        return self.convert_value_to_mv(value)
        
    def convert_value_to_mv(self, value):
        if value < 32768:
            value = (value * 1000) / 32767
        else:
            value = (((value - (2**16)) * 10000) / 32767)
        return value

    def convert_all_values_to_mv(self):
        for cavity in [self.CAV_A, self.CAV_B]:
            for signal in self.SIGNALS:
                self._signals[cavity][signal] = map(self.convert_value_to_mv,
                                                    self._raw_signals[cavity][signal]#[::338]
                                                   )

    def get_signals(self, cavity):
        return self._signals[cavity]

    def get_raw_signals(self, cavity):
        return self._raw_signals[cavity]

    # def get_indexes(self):
    #     indexes = np.where(self.read_values == self.comma)[1]
    #     return indexes
    #
    # def clear_pre_data(self):
    #     self.reduced_values = self.read_values[0, self.comma_indexes[0]:]

if __name__ == '__main__':
    DIAG_FILENAME = '../../test/data/Diags20140702162255 - default.dat'
    data_extractor = FDLDataExtractor(DIAG_FILENAME)
    data_extractor.extract_values()
    signals = data_extractor.get_signals(data_extractor.CAV_A)
    raw = data_extractor.get_raw_signals(data_extractor.CAV_A)

    from scipy import *
    import matplotlib.pyplot as plt

    plt.plot(signals['IFwLoad'])
    plt.show()
    plt.plot(raw['IFwLoad'])
    plt.show()

    plt.imshow(signals[data_extractor.CAV_A]['IrvTet1'])
    #savefig('IrvTet1')

    #import subprocess
    #subprocess.call('taurusplot' + signals['IrvTet1'] )

    import pyqtgraph as pg
    # pg.plot(signals['IFwLoad'])
    # pg.plot([1,2,3,4])

    win = pg.GraphicsWindow()
    win.addPlot(row=0, col=0, y=raw['IrvTet1'])
    win.addPlot(row=0, col=1, y=raw['QrvTet1'])
    win.addPlot(row=1, col=0, y=signals['IrvTet1'])
    win.addPlot(row=1, col=1, y=signals['QrvTet1'])

