import itertools
import math
import random
import sys

DEBUG = 0
AUTO_ANSWER = 0 # Whether we want the computer to answer itself.

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
  if matches != num_blacks:
    return True
  # Consider that there cannot be any more matching colors than whites.
  if color_match != (num_blacks + num_whites):
    return True 
  return False
 
def _PossAns2(guess, num_blacks, num_whites, possibles):
  new_possibles = []
  for possible in possibles:
    if not _InvalidSolution(num_blacks, num_whites, guess, possible):
      new_possibles.append(possible)
  return new_possibles



def _ChooseMaxDistinct(guesses):
  """Chooses the guess with the most number of distinct colors."""
  if not guesses:
    raise AssertionError('Cannot choose amongst no guesses.')
  max_size = 0
  best_guess = None
  for guess in guesses:
    cur_size = len(set(guess))
    if cur_size > max_size:
      max_size = cur_size
      best_guess = guess
  return best_guess

def _ChooseNColor(guesses, n):
  """Choose guess with exactly n colors, or most colors if possible."""
  cur_guess = None
  for guess in guesses:
    cur_size = len(set(guess))
    cur_guess = guess
    if cur_size == n:
      return guess
  return _ChooseMaxDistinct(guesses)

def _ChooseBestGuess(guesses, num_guesses):
  num_strategies = 3
  which_strategy = num_guesses % num_strategies
  if which_strategy == 0:
    return _ChooseMaxDistinct(guesses)
  elif which_strategy == 1:
    return _ChooseMaxDistinct(guesses)
    #return _ChooseNColor(guesses, 2)
  elif which_strategy == 2:
    return _ChooseMaxDistinct(guesses)
    #return _ChooseNColor(guesses, 3) 
 

class Guesser(object):
  
  def __init__(self):
    self.num_guesses = 0
    self.possibles = self._MakePossibles(NUM_CHARS, NUM_SPACES)

  def Guess(self):
    """Returns a tuple that represents the guess and removes it from a future
      possibility.
    """
    self.num_guesses += 1
    # Get 10 random possibilities and choose the one with the most number of
    # distinct colors.
    num_poss = len(self.possibles)
    print 'Number of possibilities: %d' % num_poss
    num_guesses = min(32500, num_poss)
    guesses = [self._GuessRandom(num_poss) for _ in xrange(num_guesses)]
    el = _ChooseBestGuess(guesses, self.num_guesses)
    self.possibles.remove(el)
    return el

  def _GuessRandom(self, num_poss):
    guess_rand = int(math.floor(random.random() * num_poss))
    el = self.possibles[guess_rand]
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
    # I think its better to shuffle the possibilities I ask about.
    # random.shuffle(self.possibles)
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
  index_used_for_black = []
  # Fill blacks.
  index = 0
  for cur_ans_i, corr_ans_i in zip(current_ans, correct_ans):
    index += 1
    if cur_ans_i == corr_ans_i:
      num_black += 1
      left_of_answer.remove(cur_ans_i)
      index_used_for_black.append(index)
  # Fill whites.
  index = 0
  for cur_ans_i, corr_ans_i in zip(current_ans, correct_ans):
    index += 1
    if index in index_used_for_black:
      continue
    if cur_ans_i in left_of_answer:
      num_white += 1
      print 'Cur ans i match: %s' % str(cur_ans_i)
      # Pop off that we used this color to count towards a white.
      print 'left: %s' % str(left_of_answer)
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
  N = 10
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
