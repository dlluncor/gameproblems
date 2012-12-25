import itertools
import math
import random
import sys

DEBUG = 0
AUTO_ANSWER = 1 # Whether we want the computer to answer itself.

def AssertIn(obj, item):
  if obj not in item:
    raise AssertionError('%s not in %s' % (obj, item))


# Colors range from '0' to 'NUM_CHARS - 1'
NUM_CHARS = 8
NUM_SPACES = 5

VALID_CHARS = [str(ind) for ind in xrange(NUM_CHARS)]

def _Translate(my_guess):
  """Converts my guess into colors."""
  d = {'0': 'R', '1': 'O', '2': 'Y', '3': 'G', '4': 'Blu', '5': 'W',
       '6': 'Br', '7': 'Black'}
  trans = []
  for char in my_guess:
    trans.append(d[char])
  return ' '.join(trans) 

def _InvalidSolution(num_blacks, num_whites, guess, potential_sol):
  """If there are more than num_blacks exact overlaps, it is an invalid solution."""
  matches = 0
  color_match = 0
  assert len(guess) == len(potential_sol)
  left_of_guess = list(guess)
  for guess_i, pot_sol_i in zip(guess, potential_sol):
    if guess_i == pot_sol_i:
      matches += 1
    if pot_sol_i in left_of_guess:
      color_match += 1
      left_of_guess.remove(pot_sol_i)
  if matches > num_blacks:
    return True
  # Consider that there cannot be any more matching colors than whites.
  if color_match > (num_blacks + num_whites):
    return True 
  return False
 
def _PossAns2(guess, num_blacks, num_whites, possibles):
  new_possibles = []
  for possible in possibles:
    if not _InvalidSolution(num_blacks, num_whites, guess, possible):
      new_possibles.append(possible)
  return new_possibles

class Guesser(object):
  
  def __init__(self):
    self.num_guesses = 0
    self.possibles = self._MakePossibles(NUM_CHARS, NUM_SPACES)

  def Guess(self):
    """Returns a tuple that represents the guess and removes it from a future
      possibility.
    """
    self.num_guesses += 1
    num_poss = len(self.possibles)
    print 'Number of possibilities: %d' % num_poss
    guess_rand = int(math.floor(random.random() * num_poss))
    el = self.possibles[guess_rand]
    self.possibles.remove(el)
    return el 

  def Prune(self, guess, whites, blacks):
    """User input is number of whites, number of blacks.
    
    Args:
      guess: Tuple with the current guess.
      whites:
      blacks:
    """
    if DEBUG:
      print 'Current answer: %s' % str(guess)
      print 'Num whites: %d' % whites
      print 'Num blacks: %d' % blacks
    self.possibles = _PossAns2(guess, blacks, whites, self.possibles)
    if DEBUG:
      print 'Possible solutions are: %s' % str(now_possibles)
    # Find the union of previous possible answers and my possible answers.
    if DEBUG:
      #print 'Union of possibles is: %s' % str(self.possibles)
      pass

  def _MakePossibles(self, num_chars, num_spaces):
    """Creates a list of tuples for all possible numbers."""
    valid_chars = ''.join(VALID_CHARS)
    #valid_chars = '01234567'
    return [a for a in itertools.product(valid_chars, repeat=NUM_SPACES)]

def _DetermineWhiteBlack(current_ans, correct_ans):
  """
  Args:
    current_ans: my current guess tuple.
    correct_ans: the correct answer tuple.
  Returns:
    (num_black, num_white) a user would respond with.
  """
  num_white = 0
  num_black = 0
  left_of_answer = list(correct_ans)
  for cur_ans_i, corr_ans_i in zip(current_ans, correct_ans):
    if cur_ans_i == corr_ans_i:
      num_black += 1
    elif cur_ans_i in left_of_answer:
      num_white += 1
      # Pop off that we used this color to count towards a white.
      left_of_answer.remove(cur_ans_i)
  return (num_black, num_white)

def _GetFeedback(current_ans, correct_ans):
  """Get feedback from the user or make the computer figure out the answer.

  Args:
    current_ans: my current guess tuple.
    correct_ans: the correct answer tuple.
  """
  if AUTO_ANSWER:
    (num_black, num_white) = _DetermineWhiteBlack(current_ans, correct_ans)
    return '%d %d' % (num_black, num_white)  #'1 0'
  else:
    print 'Enter %d pegs with a space (3b 2w):' % NUM_SPACES
    return raw_input()

def StartGuessing(ans):
  """
  Args:
    ans: the answer as a string, e.g., 12121
  Returns:
    The number of guesses it takes to solve this problem.
  """
  ans_tup = tuple([char for char in ans])
  for char in ans_tup:
    if char not in VALID_CHARS:
      print 'Your secret must be in the range %s' % str(VALID_CHARS)
      return
  print 'Your guess is: %s' % str(_Translate(ans))
  correct = False
  guesser = Guesser()
  while not correct:
    curans = guesser.Guess()
    print 'Myyy guess is: %s' % str(_Translate(curans))
    if curans == ans_tup:
      if AUTO_ANSWER:
        correct = True
      else:
        correct = False #Let's go forever! Playing with a human.
    else:
      myfeedback = _GetFeedback(curans, ans_tup) 
      (blacks, whites) = myfeedback.split(' ')
      print 'Blacks: %d, Whites: %d' % (int(blacks), int(whites))
      guesser.Prune(curans, int(whites), int(blacks))
  print 'Num guesses: %d' % guesser.num_guesses
  return guesser.num_guesses

def Simulate(ans):
  N = 100
  guess_list = [StartGuessing(ans) for _ in xrange(N)]
  avg = sum(guess_list) / N
  print '-' * 20
  print 'Guesses amounts: %s' % str(guess_list)
  print 'Average number of guesses: %f' % avg
  x2_list = [guess_num * guess_num for guess_num in guess_list] 
  stdev = math.sqrt(sum(x2_list)/N - math.pow(sum(guess_list)/N, 2))
  print 'Standard deviation: %f' % stdev
 
def main(argv):
  if len(argv) < 2:
    print 'Print your %d length secret with characters 0 to %d' % (NUM_SPACES,
        NUM_CHARS - 1)
    return
  if len(argv[1]) != NUM_SPACES:
    print 'Your secret must be %d characters long' % NUM_SPACES
    return
  ans = argv[1] # '1211'
  Simulate(ans)

if __name__ == '__main__':
  main(sys.argv)


#### Testing.
class Tester(object):
  
  def TestGuesser(self):
    guesser = Guesser()
