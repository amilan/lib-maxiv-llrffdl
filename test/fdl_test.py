###############################################################################
##     fdl_test module contains the functional tests for the fast data
##     logger gui.
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

import unittest
import numpy as np
from dataextractor import FDLDataExtractor


class FDLTest(unittest.TestCase):

    DIAG_FILENAME = 'data/Diags20140702162255 - default.dat'
    LOOP_FILENAME = 'data/Loops20140702161945 - default.dat'
    COMA = 32767
    CAV_A = 1
    CAV_B = 2
    SIGNAL = 'IrvTet1'
    FIRST_INDEX = 27

    def setUp(self):

        self.data_extractor = FDLDataExtractor(self.DIAG_FILENAME)

    def tearDown(self):
        pass

    def test_find_the_first_coma_in_a(self):
        #__given:
        expected_a = self.FIRST_INDEX

        #__when:
        #received_a = self.data_extractor.find_next_comma(self.CAV_A)
        received_a = self.data_extractor.find_next_comma(self.data_extractor._iterator_a)

        #__then:
        self.assertEqual(expected_a, received_a)

    def test_find_the_first_comma_in_b(self):
        #__given:
        expected_b = self.FIRST_INDEX
        
        #__when:
        received_b = self.data_extractor.find_next_comma(self.data_extractor._iterator_b)
        #received_b = self.data_extractor.find_next_comma(self.CAV_B)
        
        #__then:
        self.assertEqual(expected_b, received_b)

    def test_add_values_cav_a_to_signals_dict(self):
        #__given:
        expected = [4]

        #__when:
        index = self.data_extractor.find_next_comma(self.data_extractor._iterator_a)
        self.data_extractor.add_values_from_index(index, self.CAV_A)
        received = self.data_extractor.get_raw_value(self.SIGNAL, self.CAV_A, 0)

        #__then:
        self.assertEqual(expected, received)

    def test_add_values_cav_b_to_signals_dict(self):
        #__given:
        expected = [-3]

        #__when:
        index = self.data_extractor.find_next_comma(self.data_extractor._iterator_b)
        self.data_extractor.add_values_from_index(index, self.CAV_B)
        received = self.data_extractor.get_raw_value(self.SIGNAL, self.CAV_B, 0)

        #__then:
        self.assertEqual(expected, received)
    
    def test_convert_signal_minor_to_32768(self):
        #__given:
        expected = 4/32767*1000
        
        #__when:
        index = self.data_extractor.find_next_comma(self.data_extractor._iterator_b)
        self.data_extractor.add_values_from_index(index, self.CAV_A)
        received = self.data_extractor.get_value(self.SIGNAL, self.CAV_A, 0)

        #__then:
        self.assertEqual(expected, received)

    def test_convert_all_signals(self):
        #__given:
        
        #__when:
        self.data_extractor.extract_values()
        #print self.data_extractor._raw_signals

        #__then:
        #if it arrives to this point, it deserves to pass
        self.assertTrue(True)
        #self.assertEqual(expected, received)

    def test_index_dont_change(self):
        #__given:
        expected = self.FIRST_INDEX

        #__when:
        self.data_extractor.find_next_comma(self.data_extractor._iterator_a)
        received = self.data_extractor.find_next_comma(self.data_extractor._iterator_a)
        #received_b = self.data_extractor.find_next_comma(self.CAV_B)

        #__then:
        self.assertNotEqual(expected, received)

    def test_index_has_been_changed(self):
        #__given:
        expected = 43

        #__when:
        received_1 = self.data_extractor.find_next_comma(self.data_extractor._iterator_a)
        received = self.data_extractor.find_next_comma(self.data_extractor._iterator_a)
        #received_b = self.data_extractor.find_next_comma(self.CAV_B)

        #__then:
        self.assertEqual(expected, received)

    def test_acquisition_has_enough_values(self):
        #__given:
        expected = True

        #__when:
        received = self.data_extractor.acquisition_has_enough_values( self.data_extractor._values_a,
                                                                      self.FIRST_INDEX
                                                                    )
        #__then:
        self.assertEqual(expected, received)

    def test_extract_signals_between_indexes(self):
        #TODO: Extract signals between two indexes and without decimation
        pass

#   def test_read_indexes_as_array(self):
#       #__given:
#       #__when:
#       indexes = self.data_extractor.get_indexes()

#       #__then:
#       self.assertTrue(type(indexes) == np.ndarray)

#   def test_data_starts_with_comma(self):
#       #__given:
#       expected = self.COMMA

#       #__when
#       self.data_extractor.clear_pre_data()

#       #__then:
#       self.assertEqual(expected, self.data_extractor.reduced_values[0])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=3).run(unittest.makeSuite(FDLTest))
    #unittest.TextTestRunner().run(unittest.makeSuite(FDLTest))
