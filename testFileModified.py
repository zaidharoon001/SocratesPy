
from nodes import Var, Term, Fact, BinOp, Goals, Rule, Rules
from knowledgeBase import KnowledgeBase
from visitors import make_expr
from unificationVisitor import Substitutions
import utils
lovely_rules = KnowledgeBase({'loves/2': [Rule(Fact('loves/2', [Term('hanna'), Term('miles')]), None), Rule(Fact('loves/2', [Term('tom'), Term('tom')]), None), Rule(Fact('loves/2', [Term('simon'), Term('sara')]), None)], 'narcissist/1': [Rule(Fact('narcissist/1', [Var('X')]), Fact('loves/2', [Var('X'), Var('X')]))]})
for (_, sub) in lovely_rules.lookup(
Fact('loves/2', [Var('M'), Var('Z')])):
    print(sub)
print('# Narcissist')
for (_, sub) in lovely_rules.lookup(
Fact('narcissist/1', [Var('Y')])):
    print(sub)
print('---~~Living~~---')
life_rules = KnowledgeBase({'human/1': [Rule(Fact('human/1', [Term('miles')]), None), Rule(Fact('human/1', [Term('samael')]), None), Rule(Fact('human/1', [Term('socrates')]), None)], 'male/1': [Rule(Fact('male/1', [Term('samael')]), None), Rule(Fact('male/1', [Term('jordon')]), None), Rule(Fact('male/1', [Term('jim')]), None)], 'mortal/1': [Rule(Fact('mortal/1', [Var('X')]), Fact('human/1', [Var('X')])), Rule(Fact('mortal/1', [Var('Z')]), Fact('boy/1', [Var('Z')]))], 'boy/1': [Rule(Fact('boy/1', [Var('A')]), Goals([Fact('male/1', [Var('A')]), Fact('human/1', [Var('A')])]))], 'parent/2': [Rule(Fact('parent/2', [Term('miles'), Term('samael')]), None), Rule(Fact('parent/2', [Term('sara'), Term('samael')]), None), Rule(Fact('parent/2', [Term('amanda'), Term('samael')]), None), Rule(Fact('parent/2', [Term('steven'), Term('jordon')]), None), Rule(Fact('parent/2', [Term('laura'), Term('jordon')]), None), Rule(Fact('parent/2', [Term('cassandra'), Term('jim')]), None)], 'father/2': [Rule(Fact('father/2', [Var('A'), Var('X')]), Goals([Fact('parent/2', [Var('A'), Var('X')]), Fact('male/1', [Var('X')])]))], 'sibiling/2': [Rule(Fact('sibiling/2', [Var('A'), Var('B')]), Goals([Fact('father/2', [Var('A'), Var('X')]), Fact('father/2', [Var('B'), Var('X')])]))], 'child/2': [Rule(Fact('child/2', [Var('X'), Var('A')]), Fact('father/2', [Var('A'), Var('X')]))]})
print('# Mortal')
for (_, sub) in life_rules.lookup(
Fact('mortal/1', [Var('O')])):
    print(sub)
print('# Sibilings')
for (_, sub) in life_rules.lookup(
Fact('sibiling/2', [Term('sara'), Var('M')])):
    print(sub)
print('# Children')
for (_, sub) in life_rules.lookup(
Fact('child/2', [Term('jordon'), Var('C')])):
    print(sub)
print('---~~Addition~~---')
addition_rules = KnowledgeBase({'add/3': [Rule(Fact('add/3', [Term(0), Var('X'), Var('X')]), None), Rule(Fact('add/3', [Fact('s/1', [Var('X')]), Var('Y'), Fact('s/1', [Var('Z')])]), Fact('add/3', [Var('X'), Var('Y'), Var('Z')]))]})
for (unifier, sub) in addition_rules.lookup(
Fact('add/3', [Fact('s/1', [Fact('s/1', [Term(0)])]), Var('A'), Fact('s/1', [Fact('s/1', [Fact('s/1', [Fact('s/1', [Fact('s/1', [Term(0)])])])])])])):
    print(utils.str_dict(Substitutions.optionally_resolve(unifier.env)), 'results in', sub)
for (_, sub) in addition_rules.lookup(
Fact('add/3', [Var('A'), Fact('s/1', [Var('A')]), Fact('s/1', [Fact('s/1', [Fact('s/1', [Term(0)])])])])):
    print(sub)
print('---~~List~~---')
lst_rules = KnowledgeBase({'lst/1': [Rule(Fact('lst/1', [Term('nil')]), None), Rule(Fact('lst/1', [Fact('cons/2', [Var('L'), Var('X')])]), Fact('lst/1', [Var('X')]))], 'lst_length/2': [Rule(Fact('lst_length/2', [Term('nil'), Term(0)]), None), Rule(Fact('lst_length/2', [Fact('cons/2', [Var('X'), Var('Xs')]), Var('L')]), Goals([Fact('lst_length/2', [Var('Xs'), Var('N')]), BinOp(Var('L'), '==', BinOp(Var('N'), '+', Term(1)))]))], 'lst_member/2': [Rule(Fact('lst_member/2', [Var('X'), Fact('cons/2', [Var('X'), Var('M')])]), None), Rule(Fact('lst_member/2', [Var('X'), Fact('cons/2', [Var('P'), Var('TAIL')])]), Fact('lst_member/2', [Var('X'), Var('TAIL')]))], 'lst_concat/3': [Rule(Fact('lst_concat/3', [Term('nil'), Var('L'), Var('L')]), None), Rule(Fact('lst_concat/3', [Fact('cons/2', [Var('X1'), Var('L1')]), Var('L2'), Fact('cons/2', [Var('X1'), Var('L3')])]), Fact('lst_concat/3', [Var('L1'), Var('L2'), Var('L3')]))]})
lst1 = Fact('cons', [Term('x'), Fact('cons', [Term('y'), Term('nil')])])
lst2 = Fact('cons', [Term('a'), Fact('cons', [Term('b'), Term('nil')])])
for (_, sub) in lst_rules.lookup(make_expr(Fact('lst_member', [Term('x'), lst1]))):
    print(sub)
print('# Concatenation')
for (unifier, _) in lst_rules.lookup(
Fact('lst_concat/3', [Fact('cons/2', [Term('x'), Fact('cons/2', [Term('y'), Term('nil')])]), Fact('cons/2', [Term('a'), Fact('cons/2', [Term('b'), Term('nil')])]), Var('Res')])):
    print(utils.dict_as_eqs(Substitutions.optionally_resolve(unifier.env)))
print('# Count Members')
for (unifier, _) in lst_rules.lookup(
Fact('lst_length/2', [Fact('cons/2', [Term('a'), Fact('cons/2', [Term('b'), Fact('cons/2', [Term('c'), Term('nil')])])]), Var('N')])):
    print(utils.dict_as_eqs(Substitutions.optionally_resolve(unifier.env)))
print('---~~Numbers~~---')
lst_rules = KnowledgeBase({'semantic_trial/3': [Rule(Fact('semantic_trial/3', [Var('X'), Var('Y'), Var('Z')]), Goals([BinOp(Var('Y'), '==', BinOp(Var('X'), '+', Term(1))), Fact('inc/2', [Var('Y'), Var('Z')]), BinOp(Var('Z'), '==', BinOp(Var('X'), '+', Term(2)))]))], 'inc/2': [Rule(Fact('inc/2', [Var('X'), Var('Y')]), BinOp(Var('Y'), '==', BinOp(Var('X'), '+', Term(1))))], 'fac/2': [Rule(Fact('fac/2', [Term(0), Term(1)]), None), Rule(Fact('fac/2', [Var('N'), Var('F')]), Goals([BinOp(Var('N'), '>', Term(0)), BinOp(Var('F1'), '>', Term(0)), BinOp(Var('N1'), '==', BinOp(Var('N'), '-', Term(1))), BinOp(Var('F'), '==', BinOp(Var('N'), '*', Var('F1'))), Fact('fac/2', [Var('N1'), Var('F1')])]))]})
for (_, sub) in lst_rules.lookup(
Fact('semantic_trial/3', [Var('L'), Term(8), Var('N')])):
    print(sub)
print('# Factorial')
for (unifier, _) in lst_rules.lookup(
Fact('fac/2', [Term(4), Var('F')])):
    print(utils.dict_as_eqs(Substitutions.optionally_resolve(unifier.env)))
