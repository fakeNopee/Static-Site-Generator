import unittest

from blocktype import *





class TestBlockType(unittest.TestCase):
    def test_blocktype_list(self):
        block = '''
- list that 
- is ordered 
- jgsdnjdfgdskjsgkkgdsmkgk
'''

        self.assertEqual(block_to_block_type(block), BlockType.unordered_list)

        block = '''
1. stuff and stuff
2. testing something
3. what is this
4. still ordered
'''
        
        self.assertEqual(block_to_block_type(block), BlockType.ordered_list)

    def test_blocktype_quote(self):

        block = '''
> stuff and stuff
> testing something
> what is this
> still ordered
'''
        
        self.assertEqual(block_to_block_type(block), BlockType.quote)


    def test_blocktype_code(self):
        
        block = '''
```
stuff and stuff
testing something
what is this
still ordered
```
'''
        
        self.assertEqual(block_to_block_type(block), BlockType.code)

        block = '''
```
stuff and stuff
testing something
what is this
still ordered
```'''
        
        self.assertEqual(block_to_block_type(block), BlockType.code)

        block = '''```
stuff and stuff
testing something
what is this
still ordered
```'''
        
        self.assertEqual(block_to_block_type(block), BlockType.code)


    def test_blocktype_heading(self):


        block = "## stuff stuff and stuff"
       
        self.assertEqual(block_to_block_type(block), BlockType.heading)

        block = "###### stuff stuff and stuff"
       
        self.assertEqual(block_to_block_type(block), BlockType.heading)
        
        block = "####### stuff stuff and stuff"
       
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)
        
        block = "# stuff stuff and stuff"
       
        self.assertEqual(block_to_block_type(block), BlockType.heading)


    def test_blocktype_paragraph(self):
        block = " # stuff stuff and stuff"
       
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

        block = "#stuff stuff and stuff"
       
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)

        block = " stuff stuff and stuff"
       
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)


        block = '''# stuff
- list that 
- is ordered 
- jgsdnjdfgdskjsgkkgdsmkgk

1. stuff and stuff
2. testing something
3. what is this
4. still ordered


> stuff and stuff
> testing something
> what is this
> still ordered
'''
        self.assertEqual(block_to_block_type(block), BlockType.paragraph)