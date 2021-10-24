"""
Introducing GOTO statement into Python.

"Your scientists were so preoccupied with whether or not they could, they didn’t stop to think if they should."

Should we call it QPython now *grimace*
"""
import dis
from types import CodeType

DEBUG = True
GOTO_TOKEN = '#GOTO_'
LABEL_TOKEN = '#GOTOLABEL_'
INST_TO_REPLACE = 'LOAD_CONST'
JUMP_OP_CODE = dis.opmap.get('JUMP_ABSOLUTE').to_bytes(1, byteorder='little')

def fix_function(func, payload):
  """ Patches function with a new CodeObject where the 
      bytecode has been replaced with new.

      Credit: Artem Golubin
      Url: https://rushter.com/blog/python-bytecode-patch/
  """
  fn_code = func.__code__
  print(fn_code.co_argcount)
  func.__code__ = CodeType(fn_code.co_argcount,
                           fn_code.co_posonlyargcount,
                           fn_code.co_kwonlyargcount, 
                           fn_code.co_nlocals,
                             fn_code.co_stacksize,
                             fn_code.co_flags,
                             payload,
                             fn_code.co_consts,
                             fn_code.co_names,
                             fn_code.co_varnames,
                             fn_code.co_filename,
                             fn_code.co_name,
                             fn_code.co_firstlineno,
                             fn_code.co_lnotab,
                             fn_code.co_freevars,
                             fn_code.co_cellvars,
                             )
  
CodeType
def goto_mutator(f):
  """ Patches decorated function to allow "goto statements"
  """
  def inner_func():
    pass

  code_obj = f.__code__
  byte_code = code_obj.co_code
  consts = code_obj.co_consts
  
  index_to_label_map = {}
  for index, const in enumerate(consts):
    if isinstance(const, str) and (GOTO_TOKEN in const or LABEL_TOKEN in const):
      prefix, label_name = const.split('_', 1)
      prefix += '_'
      index_to_label_map[index] = (label_name, prefix)

  jmp_table = {}
  for inst in dis.get_instructions(f):
    if inst.opname == INST_TO_REPLACE:
      lbl_or_jmp_location = index_to_label_map.get(inst.arg)
      if lbl_or_jmp_location:
        label, prefix = lbl_or_jmp_location
        jmp_table.setdefault(label, {}).setdefault(prefix, []).append(inst.offset)
 
  patched_bytecode = []
  last_offset = 0
  for inst in dis.get_instructions(f):
    if inst.opname == INST_TO_REPLACE \
    and inst.arg in index_to_label_map:

      label_name, prefix = index_to_label_map[inst.arg]
      
      if prefix == GOTO_TOKEN: 
        jmp = jmp_table[label_name]
        # jmp_indxs = jmp.get(GOTO_TOKEN)
        lbl_indxs = jmp.get(LABEL_TOKEN)
    
        if not lbl_indxs:
          raise ValueError('Label not defined')
      
        if len(lbl_indxs) > 1:
          raise ValueError(f'Label redifinitions at bytecode offsets {lbl_indxs}')

        label_index = lbl_indxs[0]
        patched_bytecode += \
          byte_code[last_offset:inst.offset] + JUMP_OP_CODE + label_index.to_bytes(1, byteorder='little')
      
        last_offset = inst.offset + 2
      
  patched_bytecode += byte_code[last_offset:]
  fix_function(f, bytes(patched_bytecode))
  
  if DEBUG:
    print('JUMP TABLE IS:\n', jmp_table, '\n')
    print('Original ByteCode:')
    print(byte_code.hex(), '\n')
    print('ByteCode patched with GOTO\'s')
    print(bytes(patched_bytecode).hex(), '\n')

  return f

@goto_mutator  
def mutate_me(b):
  c = 7
  x = '#GOTO_something' # Actual GOTO statement NOTE: these must inline/ constant strings
  a = 1 + b
  pass
  pass
  pass
  print('DID NOT SKIP PRINT')
  x = '#GOTOLABEL_something' # The goto label
  print('WENT TO LABEL')


mutate_me(3)






