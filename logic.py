#Amy Chen acs9098
#Div Dasani dmd8603
#All group members were present and contributing during all work on this project

from read import *
from bindings import *

class fact(object):
    def __init__(self, statement, supported_by=[]):
        self.statement = statement
        if not supported_by:
            self.asserted = True
        else:
            self.asserted = False

        self.supported_by = supported_by

    def __str__(self):
        return "Fact: " + str(self.statement)

    def __eq__(self, other):
        return self.statement == other.statement


class rule(object):
    def __init__(self, rule, supported_by=[]):
        self.LHS = rule[0]
        self.RHS = rule[1]

        if not supported_by:
            self.asserted = True
        else:
            self.asserted = False

        self.supported_by = supported_by

    def __str__(self):
        return "Rule: " + str([self.LHS,self.RHS])

    def __eq__(self,other):
        return [self.LHS,self.RHS] == [other.LHS,other.RHS]

#checks if element is fact
def factq(element):
    return type(element[0]) is str
#checks if element is rule
def ruleq(element):
    return type(element[0]) is list
#checks if element is variable
def varq(element):
	return element[0] == "?"

class kb(object):
    def __init__(self):
        self.facts = []
        self.rules = []

    def add_fact(self, fact):
        self.facts.append(fact)

    def add_rule(self, rule):
        self.rules.append(rule)

    def rem_fact(self, fact1):
        self.facts.remove(fact1)

    def rem_rule(self, rule):
        self.rules.remove(rule)

    def __str__(self):
        return "KB: # of Facts: " + str(len(self.facts)) + " # of Rules: " + str(len(self.rules))

    #takes statement (a list) as input
    #adds statement as fact or rule to knowledge base
    #checks if anything can be inferred from new statement and existing facts and rules
    #adds inferred facts or rules if they exist
    def kb_assert(self, statement,support=[]):
        if factq(statement):
            f = fact(statement,support)
            self.add_fact(f)
            if not support:
                print "\nAsserting fact " + str(statement)
            else:
                print "\tInferring new fact " + str(statement)

            #cycles through all rules to see if new facts can be inferred from added fact and current rule-base
            for r1 in self.rules:
                inferred = self.infer(f, r1)
                self.assertCheck(inferred)

        elif ruleq(statement):
            r = rule(statement,support)
            self.add_rule(r)
            if not support:
                print "\nAsserting rule " + str(statement)
            else:
                print "\tInferring new rule " + str(statement)

            # cycles through all facts to see if new facts can be inferred from added fact and current rule-base
            for f1 in self.facts:
                inferred = self.infer(f1, r)
                self.assertCheck(inferred)

    #checks if inferred fact or rule is already in knowledge base
    #if it is and it was not asserted, add to supported_by
    #if it is and it was asserted,leave the asserted fact or rule
    #otherwise add the fact or rule
    def assertCheck(self,inferred):
        exists = False
        if type(inferred) is fact:
            for ifact in self.facts:
                if inferred.statement == ifact.statement:
                    if not ifact.asserted and inferred.supported_by not in ifact.supported_by:
                        ifact.supported_by.extend(inferred.supported_by)
                    exists = True
            if not exists:
                self.kb_assert(inferred.statement,inferred.supported_by)
        elif type(inferred) is rule:
            for irule in self.rules:
                if [inferred.LHS, inferred.RHS] == [irule.LHS, irule.RHS]:
                    if not irule.asserted and inferred.supported_by not in irule.supported_by:
                        irule.supported_by.extend(inferred.supported_by)
                    exists = True
            if not exists:
                self.kb_assert([inferred.LHS,inferred.RHS],inferred.supported_by)

    # takes bindings (the object) and a statement(a list) as input
    # returns a statement (a list) with variables bound as in bindings
    def kb_instantiate(self, bindings, statement):
        if factq(statement):
            return map(lambda (x): bindings.binding_value(x) if bindings.binding_value(x) else x, statement)
        elif ruleq(statement):
            return map(lambda (y): map(lambda (x): bindings.binding_value(x) if bindings.binding_value(x) else x,y),statement)

    # takes a fact and rule as input
    # returns fact or rule with supporting fact and rule
    # returns false if nothing can be inferred
    def infer(self, fact1, rule1):
        if len(rule1.LHS) == 1:
            if match(fact1.statement, rule1.LHS[0]):
                new = self.kb_instantiate(match(fact1.statement, rule1.LHS[0]), rule1.RHS)
                print "\tInferring from " + str(fact1) + " and " + str(rule1)
                return fact(new, [[fact1, rule1]])
        else:
            if match(fact1.statement, rule1.LHS[0]):
                bindings = match(fact1.statement, rule1.LHS[0])
                rL = self.kb_instantiate(bindings, rule1.LHS)
                rR = self.kb_instantiate(bindings, rule1.RHS)
                rL.remove(rL[0])

                print "\tInferring from " + str(fact1) + " and " + str(rule1)
                return rule([rL, rR], [[fact1, rule1]])
        return False

    #takes statement (a list) as input
    #takes boolean supported, which indicates if this statement was supported by a fact or rule that was retracted
    #removes statement from knowledge base
    #removes facts and rules supported by statement
    def kb_retract(self,statement,supported = False):
        info = self.matcher(statement)
        remove = []

        #loops through all facts in knowledge base to remove ones supported by statement
        for k in self.facts:
            #checks if statement is the only fact or rule that supports fact k
            #remove k if only statement supports it
            #if something else supports k, remove statement from supported_by but don't remove k
            for support in k.supported_by:
                if type(support) is not list:
                    if info == support:
                        k.supported_by.remove(support)
                        remove.append(k.statement)
                elif type(info) is fact and info == support[0] or type(info) is rule and info == support[1]:
                    while support in k.supported_by:
                        k.supported_by.remove(support)
                    if not k.supported_by:
                        remove.append(k.statement)

        # loops through all rules in knowledge base to remove ones supported by statement
        for l in self.rules:
            # checks if statement is the only fact or rule that supports rule l
            # remove l if only statement supports it
            # if something else supports l, remove statement from supported_by but don't remove l
            for support in l.supported_by:
                if type(support) is not list:
                    if info == support:
                        l.supported_by.remove(support)
                        remove.append([l.LHS,l.RHS])
                elif (type(info) is fact and info == support[0]) or (type(info) is rule and info == support[1]):
                    while support in l.supported_by:
                        l.supported_by.remove(support)
                    if not l.supported_by:
                        remove.append([l.LHS, l.RHS])

        if type(info) is fact:
            self.rem_fact(info)
            if not supported:
                print "\nRetracting fact " + str(statement)
            else:
                print "\tRemoving fact " + str(statement) + " from KB\n"
        elif type(info) is rule:
            self.rem_rule(info)
            if not supported:
                print "\nRetracting rule " + str(statement)
            else:
                print "\tRemoving rule " + str(statement) + " from KB\n"
        for r in remove:
            print "\tRemoving facts and rules supported by " + str(statement)
            self.kb_retract(r,True)

    #takes fact statement (a list) as input
    #returns list of bindings lists that hold if the statement is true
    def ask(self, query):
        bindings = map(lambda(x): match(x.statement,query),self.facts)
        bindings = filter(lambda(x): x,bindings)
        if bindings:
            return bindings
        else:
            if self.matcher(query):
                return True
            return []

    #for each statement in the list, see what bindings support it
    #ompares those bindings with bindings for all other statements
    #returns list of bindings lists of bindings all statements have in common
    def askPlus(self, queries):
        firstQuery = queries[0]
        testBindings = self.ask(firstQuery)
        remove = []

        for query in queries:
            for binding in testBindings:
                temp = self.kb_instantiate(binding,query)
                if not self.matcher(temp):
                    if self.ask(temp):
                        for b in self.ask(temp):
                            for k in b.bindings.keys():
                                value = b.binding_value(k)
                                if k not in binding.bindings.keys():
                                    bindingCopy = binding
                                    bindingCopy.add_binding(k,value)
                                    testBindings.append(bindingCopy)
                                else:
                                    bindingCopy = binding
                                    bindingCopy.bindings[k] = b.bindings[k]
                                    testBindings.append(bindingCopy)

                    remove.append(binding)
        for r in remove:
            testBindings.remove(r)
        return testBindings

    #takes fact or rule as input
    #returns facts that support statement
    def why(self,statement):
        support = []
        #check if input was a list instead of a fact or rule
        if type(statement) is not fact and type(statement) is not rule:
            support = self.matcher(statement)
        #if statement is a fact or rule
        else:
            support = statement
        if support:
            if not support.supported_by:
                print "\t" + str(support) + " - ASSERTED"
            else:
                for s in support.supported_by:
                    for i in s:
                        if not i.supported_by:
                            print "\t" + str(i) + " - ASSERTED"
                        else:
                            print "\t" + str(i)
                            self.why(i)

    #matches statement (a list) to fact or rule
    def matcher(self,statement):
        if len(statement) == 3:
            for a in self.facts:
                if a.statement == statement:
                    return a
        elif len(statement) == 2:
            for b in self.rules:
                if [b.LHS, b.RHS] == statement:
                    return b
        return False

class action(object):
    def __init__(self, preconditions=[],add=[],retract=[]):
        self.preconditions = preconditions
        self.add = add
        self.retract = retract


# match test file functions
def KB_assert(kb,assertion):
    kb.kb_assert(assertion)

def KB_ask(kb,query):
    if factq(query):
        return kb.ask(query)

def instantiate(kb,pattern, bindings):
    return kb.kb_instantiate(bindings,pattern)

def KB_retract(kb,assertion):
    if factq(assertion):
        kb.kb_retract(assertion)

def KB_why(kb,statement):
    if factq(statement):
        print "\nExplaining: " + str(statement)
        kb.why(statement)

def KB_ask_plus(kb,queries):
    return kb.askPlus(queries)