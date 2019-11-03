import unittest
from byte_reader import *
from checker import *
from mathematics import *
from zipcode import *

class TestData(unittest.TestCase):
    def test_byte_reader_module(self):
        with open('./Resources/t/1.jpg','rb') as file:
            bytes = read_byte(file, 2, 0)      
            # Read in jpg so first 2 bytes in small endian should be 0xd8ff
            self.assertEqual(bytes,b'\xd8\xff')
            
            # Change small endian to big endian 
            bytes = to_big_endian(bytes)
            self.assertEqual(bytes,b'\xff\xd8')
            
            # check if conversion yields 65496
            int_form = bytearr_to_int(bytes)
            self.assertAlmostEqual(int_form, 65496)
            
            
    def test_checker_module(self):        
        # Test if file is jpg which it is 
        self.assertTrue(test_for_jpg('./Resources/t/1.jpg'))
        
        # Test if file is EXIF which it is 
        self.assertTrue(test_for_exif('./Resources/t/1.jpg'))
        
        # Test if file store gpsinfo which it does
        self.assertTrue(test_for_gps('./Resources/t/1.jpg'))
            
            
    def test_mathematics_module(self):
        # Test if int to dec stirng works
        self.assertEqual(int_str(456,1),'456')
        
        # Test if int to hex string works 
        self.assertEqual(int_str(255,2),'0xff')
        
        # Test if int to hex string without prefix works
        self.assertEqual(int_str(255,3),'ff')
        
        # test if hex string to int works 
        self.assertEqual(str_int('0xff',1),255)
        
        # test if reverse string works
        self.assertEqual(reverse_str('pepega'),'agepep')
        
    def test_zipcode_module(self):
    
        test_coordinates = [48.855647,2.29863]
        
        # Test if we can find coordinates from EXIF image
        ltt = get_ltt_exif('./Resources/t/1.jpg')
        self.assertEqual(ltt,[38.909833,1.438667])
        
        #Test if GOOGLE CLOUD VISION ML API works 
        ltt = get_ltt_non_exif('./Resources/t/2.jpg')
        self.assertAlmostEqual(ltt,[48.855647,2.29863])
        
        # # Test if France zip code is correct
        zip_code = ltt_to_zip_from_google(test_coordinates)
        self.assertEqual(zip_code,'75007')
        
        # # test if hex string to int works 
        zip_code = ltt_to_zip_from_GeoPy(test_coordinates)
        self.assertEqual(zip_code,'75007') 
if __name__ == ("__main__"):
    unittest.main()
