import itertools
import sys

def AssertIn(obj, item):
  if obj not in item:
    raise AssertionError('%s not in %s' % (obj, item))


NUM_CHARS = 6
NUM_SPACES = 4

class Guesser(object):
  
  def __init__(self):
    self.num_guesses = 0
    self.possibles = self._MakePossibles(NUM_CHARS, NUM_SPACES)

  def Guess(self):
    self.num_guesses += 1
    num_poss = len(self.possibles)
    el = self.possibles[num_poss-1]
    self.possibles.remove(el)
    guessans = ''.join(el)
    return guessans

  def Prune(self, curans, whites, blacks):
    """User input is number of whites, number of blacks."""
    validnums = '123456'
    print 'Current answer: %s' % curans
    print 'Num whites: %d' % whites
    print 'Num blacks: %d' % blacks
    num_blank = NUM_SPACES - whites - blacks
    num_keep = NUM_SPACES - num_blank

    itertools.product()
    
    itertools.permutation(validnums, num_keep)
    

  def _MakePossibles(self, num_chars, num_spaces):
    """Creates a list of tuples for all possible numbers."""
    return [a for a in itertools.product('123456', repeat=NUM_SPACES)]
    #def _Append(cur_string, spaces_left):
    #  spaces_left -= 1
    #  if spaces_left == 0:
    #    return cur_string
    #
    #    _Append() 

class Tester(object):
  
  def TestGuesser(self):
    guesser = Guesser()
    possibles = guesser._MakePossibles(2, 3)
    AssertIn('000', possibles) 
    AssertIn('001', possibles) 
    AssertIn('010', possibles) 
    AssertIn('011', possibles) 
    AssertIn('100', possibles) 
    AssertIn('101', possibles) 
    AssertIn('110', possibles) 
    AssertIn('111', possibles) 

def main(argv):
  ans = argv[1] # '1211'
  if len(ans) != NUM_SPACES:
    print 'Your secret must be %d characters long' % NUM_SPACES
    return
  correct = False
  guesser = Guesser()
  while not correct:
    curans = guesser.Guess()
    print 'Guessing %s' % curans
    if curans == ans:
      correct = True
    else:
      myfeedback = raw_input()
      (whites, blacks) = myfeedback.split(' ')
      guesser.Prune(curans, int(whites), int(blacks))
  print 'Num guesses: %d' % guesser.num_guesses 
  

if __name__ == '__main__':
  main(sys.argv)
