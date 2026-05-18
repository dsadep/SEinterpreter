from dataclasses import dataclass


@dataclass
class NumberNode:
    value: int # | float

@dataclass
class UnaryOpNode:
    op: str
    operand: object

@dataclass
class BinaryOpNode:
    left: object
    op: str
    right: object

@dataclass
class VarNode:
    name: str
    
@dataclass
class AssignNode:
    name: str
    value: object

@dataclass 
class ProgrammNode:
    pass