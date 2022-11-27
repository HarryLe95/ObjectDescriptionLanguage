from parser import Token, Tokeniser
import unittest

class TestTokeniserLine1(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','class'), 
                                Token('identifier','A'), 
                                Token('symbol',':'), 
                                Token('identifier','B'), 
                                Token('symbol',','), 
                                Token('identifier','C'), 
                                Token('symbol',','), 
                                Token('identifier','D'),
                                Token('symbol','{')]
    
    def test_case_1(self):
        line = "class A : B , C , D {"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_2(self):
        line = "class A:B,C,D{"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_3(self):
        line = "class A : B, C, D{"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_4(self):
        line = "class A:B,C,D{ //This is a comment"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)

class TestTokeniserLine2(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','class'), 
                                Token('identifier','A'),
                                Token('symbol','{')]

    def test_case_1(self):
        line = "class A{"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_2(self):
        line = "class A {"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)

class TestTokeniserLine3(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','local'), 
                                Token('identifier','class_group'),
                                Token('symbol','='),
                                Token('identifier','B'),
                                Token('symbol',','),
                                Token('identifier','C'),
                                Token('symbol',';')]

    def test_case_1(self):
        line = "local class_group = B, C;"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_2(self):
        line = "local class_group=B,C;"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_3(self):
        line = "local class_group = B,C ;"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)

class TestTokeniserLine4(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','field'), 
                                Token('keyword','int'),
                                Token('identifier','x'),
                                Token('symbol',','),
                                Token('identifier','y'),
                                Token('symbol',';')]  
        
    def test_case_1(self):
        line = "field int x, y;"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_2(self):
        line = "field int x,y;"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
    def test_case_3(self):
        line = "field int x,y ;"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)

class TestTokeniserLine5(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','method'), 
                                Token('keyword','bool'),
                                Token('identifier','contain'),
                                Token('symbol','('),
                                Token('identifier','Point'),
                                Token('symbol',')'),
                                Token('symbol',';')]  
        
    def test_case_1(self):
        line = "method bool contain(Point);"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)

class TestTokeniserLine6(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','override'),
                                Token('keyword','method'), 
                                Token('keyword','bool'),
                                Token('identifier','contain'),
                                Token('symbol','('),
                                Token('identifier','Point'),
                                Token('symbol',')'),
                                Token('symbol',';')]  
        
    def test_case_1(self):
        line = "override method bool contain(Point);"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)

class TestTokeniserLine7(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','static'), 
                                Token('identifier','Point'),
                                Token('identifier','next'),
                                Token('symbol',','),
                                Token('identifier','prev'),
                                Token('symbol',';')]  
        
    def test_case_1(self):
        line = "static Point next, prev;"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
class TestTokeniserLine8(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','method'), 
                                Token('keyword','array'),
                                Token('symbol','<'),
                                Token('identifier','Point'),
                                Token('symbol','>'),
                                Token('identifier','getConvexHull'),
                                Token('symbol','('),
                                Token('symbol',')'),
                                Token('symbol',';')]  
        
    def test_case_1(self):
        line = "method array<Point> getConvexHull();"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
class TestTokeniserLine9(unittest.TestCase):
    def setUp(self) -> None:
        self.expected_output = [Token('keyword','method'), 
                                Token('keyword','float'),
                                Token('identifier','getDistance'),
                                Token('symbol','('),
                                Token('identifier','Point'),
                                Token('symbol',')'),
                                Token('symbol',';')]  
        
    def test_case_1(self):
        line = "method float getDistance(Point);"
        actual_output = Tokeniser(line).get_tokens()
        self.assertListEqual(self.expected_output,actual_output)
        
if __name__ == "__main__":
    unittest.main()