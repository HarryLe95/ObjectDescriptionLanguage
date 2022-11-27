from __future__ import annotations
import os 
from typing import List
import re

KEYWORD = ['class','local',
           'int','float','double','char','str','bool','duck','void',
           'array','set','map',
           'field','static','class_var',
           'override','constructor','method',
           'static_method','class_method']

SYMBOL = ['<','>','(',')','{', '}', ',', ';', ':', '.','=']

NATIVE_TYPE = ['int','float','double','char','str','bool','duck','void',
               'array','set','map']

class FileManager:
    def __init__(self, path:str|None=None):
        self.verify_path_(path)
        
    def verify_path_(self, path:str) -> None:
        if path is not None:
            self.path = path 
            self.files = self.get_oml_files(self.path)
    
    @staticmethod 
    def is_oml_file(path:str) -> bool:
        if os.path.isfile(path) and path.endswith(".oml"):
            return True 
        return False 
    
    @classmethod
    def validate_and_append_(cls, path:str, container:List[str])->None:
        if cls.is_oml_file(path):
            container.append(path)
    
    @classmethod 
    def get_oml_files(cls, path:str)->List[str]:
        oml_files = []
        if os.path.isfile(path):
            cls.validate_and_append_(path, oml_files)
        if os.path.isdir(path):
            for file in os.listdir(path):
                cls.validate_and_append_(os.path.join(path,file), oml_files)
        return oml_files

class Token:
    def __init__(self,token_type:str,token_value:str=""):
        self.token_type = token_type 
        self.token_value = token_value 
        self.token_children = []
        
    def add(self, token:Token)->None:
        self.token_children.append(token)
        
    def __str__(self,depth=0)->str:
        """
        Generate a string from self ParseTree
        @return A printable representation of self ParseTree with indentation
        """        
        # Set indentation
        indent = ""
        for i in range(0,depth):
            indent += "  \u2502 "
        
        # Generate output
        output = ""
        if(len(self.token_children)>0):
            # Output if the node has children
            output += self.token_type + "\n"
            for child in self.token_children:
                output += indent + "  \u2514 " + child.__str__(depth+1)
            
            output += indent + "\n"
        else :
            # Output if the node is a leaf/terminal
            output += self.token_type + " " + self.token_value + "\n"
        
        return output
    
    def __repr__(self)->str:
        return self.__str__()
  
    def __eq__(self, other:Token)->bool:
        if self.token_type != other.token_type:
            return False 
        if self.token_value != other.token_value:
            return False 
        if self.token_children != other.token_children:
            return False 
        return True 
  
class Compiler:
    def __init__(self, path:str):
        self.path = path 
        self.file_manager = FileManager(self.path)
        self.class_list = {} 
        self.local_variable_list = {} 

class CodeGenerator:
    pass

class ParserError(Exception):
    pass

class Tokeniser:
    identifier = re.compile(r"^[^\d\W]\w*\Z", re.UNICODE)
    
    def __init__(self,file:str):
        self.file = file 
        
    def get_tokens(self)->List[Token]|None:
        if os.path.isfile(self.file):
            return self.get_tokens_from_file(self.file)
        if isinstance(self.file,str):
            return self.get_tokens_from_line(self.file)
        return None
    
    @classmethod
    def get_tokens_from_file(self, file:str)->List[Token]|None:
        tokens = []
        with open(file, 'r') as file_: 
            hasNextLine = True 
            while hasNextLine: 
                line = file_.readline()
                if line == '':
                    hasNextLine = False
                    return tokens 
                if line == '\n':
                    continue 
                output = self.get_tokens_from_line(line)
                tokens.append(output) if isinstance(output,Token) else tokens.extend(output) 
        return tokens
    
    @classmethod 
    def remove_line_comments(self,line:str)->List[str]|None:
        line = line.split("//")[0]
        line = line.split("/*")[0]
        line = line.split("*/")[0]
        line = line.strip()
        if len(line)!=0:
            if line[0]=="*":
                return None
        return line 
    
    @classmethod 
    def is_identifier(self, token:str) -> bool:
        if re.match(self.identifier,token):
            if not(token in KEYWORD):
                return True 
        return False 
    
    @classmethod 
    def is_keyword(self, token:str) -> bool:
        if token in KEYWORD:
            return True 
        return False 
    
    @classmethod 
    def is_symbol(self,token:str)->bool:
        if token in SYMBOL:
            return True 
        return False 
    
    @classmethod 
    def contain_symbol(self, token:str):
        for s in SYMBOL:
            if s in token:
                return s
        return False 
    
    @classmethod 
    def parse_token(self,token:str)->Token|List[Token]:
        if self.is_keyword(token):
            return Token("keyword",token)
        if self.is_identifier(token):
            return Token("identifier",token)
        if self.is_symbol(token):
            return Token("symbol",token)
        else:
            tokens = [] 
            s = self.contain_symbol(token)
            if s:
                items = token.partition(s)
                for i in items:
                    if i!= "":
                        output = self.parse_token(i)
                        tokens.append(output) if isinstance(output,Token) else tokens.extend(output)
                return tokens
            else:
                raise ParserError(f"Unidentifiable token: {token}")
    
    @classmethod
    def get_tokens_from_line(self, line:str)->List[Token]|None:
        tokens = [] 
        line = self.remove_line_comments(line)
        if line is None:
            return None 
        for token in line.split(" "):
            output = self.parse_token(token)
            tokens.append(output) if isinstance(output,Token) else tokens.extend(output)
        return tokens

def expect_identifier_(token:Token, parent:Token)->None:
    if token.token_type != 'identifier':
        raise ParserError(f"{token.token_value} is not a valid identifier")
    parent.add(token)
    
def expect_keyword_(token:Token, keyword:str, parent:Token)->None:
    if token.token_type != 'keyword' or token.token_value!=keyword:
        raise ParserError(f"Expect keyword: {keyword}, Actual: {token.token_value}")
    parent.add(token)
    
def expect_symbol_(token:Token, symbol:str, parent:Token)->None:
    if token.token_type != 'symbol' or token.token_value != symbol:
        raise ParserError(f"Expected symbol: {symbol}, Actual: {token.token_value}")
    parent.add(token)
                  
class Parser:
    def __init__(self, tokens:List[Token]|None):
        self.tokens = tokens
        self.c_index = 0 
    
    @property    
    def current_token(self)->Token:
        if self.c_index < len(self.tokens):
            return self.tokens[self.c_index]
        return None 
    
    @property
    def current_value(self)->str:
        return self.current_token.token_value if self.current_token is not None else None 
    
    @property
    def current_type(self)->str:
        return self.current_token.token_type if self.current_token is not None else None 
    
    def advance(self): 
        self.c_index+=1

    def expect_identifier(self,parent:Token)->None:
        expect_identifier_(self.current_token,parent)
        self.advance()
        
    def expect_keyword(self,keyword:str,parent:Token)->None:
        expect_keyword_(self.current_token,keyword,parent)
        self.advance()
        
    def expect_symbol(self,symbol:str,parent:Token)->None:
        expect_symbol_(self.current_token,symbol,parent)
        self.advance()
    
    def compile_classname_simple(self)->Token:
        root = Token("class_name","")
        self.expect_identifier(root)
        return root 
    
    def compile_classname_general(self)->Token:
        root = Token("class_name","")
        self.expect_identifier(root)
        if self.current_value == ".":
            self.expect_symbol(".",root)
            root.add(self.compile_classname_general())
        return root 
    
    def compile_varname(self)->Token:
        root = Token("var_name","")
        self.expect_identifier(root)
        return root 
    
    def compile_var_type(self)->Token:
        root = Token("var_type","")
        if self.current_value in ['int','float','double','char','str','bool','duck','void']:
            self.expect_keyword(self.current_value,root)
            return root 
        if self.current_value in ['array','set']:
            self.expect_keyword(self.current_value,root)
            self.expect_symbol("<",root)
            root.add(self.compile_var_type())
            self.expect_symbol(">",root)
            return root 
        if self.current_value == "map":
            self.expect_keyword("map",root)
            self.expect_symbol("<",root)
            root.add(self.compile_var_type())
            self.expect_symbol(",",root)
            root.add(self.compile_var_type())
            self.expect_symbol(">",root)
            return root 
        root.add(self.compile_classname_general())
        return root
    
    def compile_methodname(self)->Token:
        root = Token("method_name","")
        self.expect_identifier(root)
        return root 
    
    def compile_local_var_dec_stmt(self) -> Token:
        root = Token("local_var_dec_stmt","")
        self.expect_keyword('local',root)
        self.expect_identifier(root)
        self.expect_symbol("=",root)
        root.add(self.compile_class_list())
        self.expect_symbol(";",root)
        return root     
    
    def compile_class_list(self)->Token:
        root = Token("class_list","")
        root.add(self.compile_classname_general())
        while (self.current_value == ','):
            self.expect_symbol(",",root)
            root.add(self.compile_classname_general())
        return root 
        
    def compile_class_dec_stmt(self)->Token:
        root = Token("class_dec_stmt","")
        self.expect_keyword("class",root)
        root.add(self.compile_classname_simple())
        if self.current_value == ":":
            self.expect_symbol(":",root)
            root.add(self.compile_class_list())
        self.expect_symbol("{",root)
        while True:
            try:
                root.add(self.compile_class_var_dec_stmt())
            except ParserError:
                try:
                    root.add(self.compile_class_method_dec_stmt())
                except ParserError:
                    break        
        self.expect_symbol("}",root)
        return root 
    
    def compile_class_var_dec_stmt(self)->Token:
        root = Token("class_var_dec_stmt","")
        if self.current_value in ['field','static','class_var']:
            self.expect_keyword(self.current_value,root)
        else:
            raise ParserError()
        root.add(self.compile_var_type())
        root.add(self.compile_varname())
        while self.current_value == ",":
            self.expect_symbol(",",root)
            root.add(self.compile_varname())
        self.expect_symbol(";",root)
        return root 
    
    def compile_class_method_dec_stmt(self)->Token:
        root = Token("class_method_dec_stmt","")
        if self.current_value == "override":
            self.expect_keyword("override",root)
        if self.current_value in ['constructor','method','static_method','class_method']:
            self.expect_keyword(self.current_value,root)
        root.add(self.compile_var_type())
        root.add(self.compile_methodname())
        self.expect_symbol("(",root)
        root.add(self.compile_type_list())
        self.expect_symbol(")",root)
        self.expect_symbol(";",root)
        return root 
        
    def compile_type_list(self)->Token:
        root = Token("type_list","")
        if self.current_type == 'identifier':
            root.add(self.compile_var_type())
            while self.current_value == ",":
                self.expect_symbol(",",root)
                root.add(self.compile_var_type())
        return root 
            
    def compile_program(self)->Token:
        root = Token("program")
        while self.current_token is not None:
            try:
                root.add(self.compile_local_var_dec_stmt())
            except ParserError:
                try:
                    root.add(self.compile_class_dec_stmt())
                except ParserError:
                    break
        return root
    
if __name__ == "__main__":
    p = Tokeniser("Point_Example.oml")
    tokens = p.get_tokens()
    parser = Parser(tokens)
    token = parser.compile_program()
    print(token)
    