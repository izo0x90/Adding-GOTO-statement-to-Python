# Adding GOTO statement into Python

"Your scientists were so preoccupied with whether or not they could, they didn’t stop to think if they should." - That JURASSIC PARK guy

You guys remember basic.

Just what it sounds like, a decorator that patches the bytecode of a decorated function to allow variable assignments to specific string constants to be treated as GOTO/JUMP statements and LABELS to jump to.

Just in case it needs to be said, yes this is a joke and has no actual uses, nor should anyone use it for anything real other than having fun.

All relevant code in main.py. 

Use:

@goto_mutator             << Decorate func you want to patch GOTOs into with mutator
some_func():
pass                      << Do regular stuff
pass
pass 
x = "#GOTO_mylabel"       << This is the goto statement, var name does not matter, statement has to be a string const, staring with key work `#GOTO_` after that label name
pass
pass
pass                      <<  Do more regular stuff, of course after patching the goto statemet will skip right over this secion
x = "#GOTOLABEL_mylabel"  << This is the LABEL we will that will be jumped to
pass 
pass                      << Keep doing stuff 

You should be able to define as many jumps and labels as desired, mutator will build a map and patch in jumps. 

Live REPL demo here:
[https://replit.com/@HristoGueorguie/Adding-GOTO-statement-to-Python-cue-eveil-laughter](https://replit.com/@HristoGueorguie/Adding-GOTO-statement-to-Python-cue-eveil-laughter).

---

Links to refs:

[https://rushter.com/blog/python-bytecode-patch/](https://rushter.com/blog/python-bytecode-patch/) - Patching bytecode article by Artem Golubin

[https://www.aosabook.org/en/500L/a-python-interpreter-written-in-python.html](https://www.aosabook.org/en/500L/a-python-interpreter-written-in-python.html) - Python Interpreter in Python article by Allison Kaptur
