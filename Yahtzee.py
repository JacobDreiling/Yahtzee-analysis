import random

categories=['ones','twos','threes','fours','fives','sixes','chance','four of a kind','full house','small straight','large straight','yahtzee']

#max possible score: 345
def score(name,dice):
	counts=[dice.count(i) for i in range(1,7)]
	units=categories[:6]
	if name in units:
		n=units.index(name)+1
		return n*counts[n-1]
	if name=='chance':
		return sum(dice)
	if name=='four of a kind':
		return sum(dice)*(4 in counts)
	if name=='full house':
		return 25*(3 in counts)*(2 in counts)
	if name=='small straight':
		straight=any([1]*4==counts[i:i+4] for i in range(3))
		return 30*straight
	if name=='large straight':
		straight=any([1]*5==counts[i:i+5] for i in range(2))
		return 40*straight
	if name=='yahtzee':
		return 50*(5 in counts)

def randomGame():
	plays=categories[:]
	random.shuffle(plays)
	upperScore=lowerScore=0
	for round in range(len(categories)):
		play=plays.pop()
		roll=[random.randint(1,6) for d in range(5)]
		points=0
		if random.random()<.5:
			points=score(play,roll) #end on roll 1
		else:
			#fyi, randomly rerolling is how a human would play Yatzee randomly
			#but it doesn't actually change the score distribution
			reroll=random.randint(1,31)
			for i in range(5):
				if reroll%2:
					roll[i]=random.randint(1,6)
				reroll//=2
			if random.random()<.5:
				points=score(play,roll) #end on roll 2
			else:
				reroll=random.randint(1,31)
				for i in range(5):
					if reroll%2:
						roll[i]=random.randint(1,6)
					reroll//=2
				points=score(play,roll) #end on roll 3
		if categories.index(play)<6:
			upperScore+=points
		else:
			lowerScore+=points
	bonus=35*(upperScore>62)
	return upperScore+bonus+lowerScore

def greedyGame():
	plays=categories[:]
	upperScore=lowerScore=0
	def find_best(roll):
		play=rec=0
		for i,p in enumerate(plays):
			s=score(p,roll)
			if s>rec:
				play=i
				rec=s
		return play,rec
	for round in range(len(categories)):
		roll=[random.randint(1,6) for d in range(5)]
		play,record=find_best(roll)
		points=0
		if record>0:
			plays.pop(play)
			points=record #end on roll 1
		else:
			reroll=random.randint(1,31)
			for i in range(5):
				if reroll%2:
					roll[i]=random.randint(1,6)
				reroll//=2
			play,record=find_best(roll)
			if record>0:
				plays.pop(play)
				points=record #end on roll 2
			else:
				reroll=random.randint(1,31)
				for i in range(5):
					if reroll%2:
						roll[i]=random.randint(1,6)
					reroll//=2
				play,record=find_best(roll)
				plays.pop(play)
				points=record #end on roll 3
		if play<6:
			upperScore+=points
		else:
			lowerScore+=points
	bonus=35*(upperScore>62)
	return upperScore+bonus+lowerScore

import matplotlib.pyplot as plt
import numpy as np

num_games=10000
scores1=[randomGame() for _ in range(num_games)]
scores2=[greedyGame() for _ in range(num_games)]
plt.close()
plt.title('Simple Yatzee Strategies')
plt.xlabel('Ranked Games')
plt.ylabel('Score')
plt.plot([0,num_games],[345]*2,'r--',label='Max score')
plt.plot(sorted(scores1),'r-',label='Random')#color=(.8,0,.4)
plt.plot(sorted(scores2),'g-',label='Greedy')#color=(.5,0,.8)
plt.legend()
plt.show()
print('Playing randomly:\nMean: %f Stdev: %f'%(np.mean(scores1),np.std(scores1)))
print('Simple greedy strategy:\nMean: %f Stdev: %f'%(np.mean(scores2),np.std(scores2)))
