import numpy as np
import matplotlib.pyplot as plt
class GA:
    def __init__(self, PopSize, NumGen, MuPerc =0.1, Nqueen=8):
        self.PopSize = PopSize
        self.NumGen = NumGen
        self.MuPerc = MuPerc
        self.Nqueen = Nqueen

    def chesDisplay(self, sol):
        n= len(sol)
        board = np.zeros((n,n))

        for col,row in enumerate(sol):
            board[row,col]=1

        fig, ax = plt.subplots(figsize = (6,6))
        ax.imshow(board, cmap='binary', extent=(0, n, 0, n))

        for i in range(n+1):
            ax.axhline(i, color='black', linewidth = 0.8)
            ax.axvline(i, color='black', linewidth = 0.8)

        for col,row in enumerate(sol):
            ax.text(col+0.5, n-row-0.5, 'Q', fontsize = 20, ha = 'center', va= 'center', color = 'red')

        ax.set_xticks([])
        ax.set_yticks([])
    def init_pop(self,):
        pop = np.random.randint(low=0, high= self.Nqueen, size=(self.PopSize, self.Nqueen), dtype = np.int8)
        return pop

    def fitness(self,state):
        attack = 0
        for i in range(self.Nqueen):
            for j in range(i+1, self.Nqueen):
                if state[i] in {state[j], state[j] + (i-j), state[j]- (i-j)}:
                    attack += 1
        return attack

    def Evaluate(self, pop):
        scores = []
        for i in pop:
            scores.append(self.fitness(i))
        return np.array(scores)

    def solver(self):
        Population = self.init_pop()
        gen = 0
        while gen <= self.NumGen:
            generation = []
            score = self.Evaluate(Population)
            scoreSorted = np.argsort(score)
            score = score[scoreSorted]
            sortedPop = Population[scoreSorted]

            popPerc = 0.6
            ToTake = np.int64(np.round(self.PopSize * popPerc))
            bestPop = sortedPop[0:ToTake]

            bestState = bestPop[0]
            bestCost = score[0]

            print(f'Best so far :{bestState} with attack :{bestCost}')

            if bestCost ==0:
                print(f'A solution is found :{bestState} with attack :{bestCost}')
                return bestState

            j=0
            while j <=self.PopSize:
                parent = np.random.choice(np.arange(0, bestPop.shape[0]), size = 2, replace=False)
                Father = parent[0]
                Mother = parent[1]

                crom1 = bestPop[Father]
                crom2 = bestPop[Mother]

                cut = np.random.randint(3,5)

                child1= np.concatenate((crom1[0:cut], crom2[cut:]))
                child2= np.concatenate((crom2[0:cut], crom1[cut:]))

                if np.random.uniform() < self.MuPerc:
                    toChange = np.random.randint(0, self.Nqueen)
                    child1[toChange] = np.random.randint(0, self.Nqueen)
                if np.random.uniform() < self.MuPerc:
                    toChange = np.random.randint(0, self.Nqueen)
                    child2[toChange] = np.random.randint(0, self.Nqueen)

                generation.append(child1)
                generation.append(child2)

                j = j+1
            Population = np.array(generation)
            gen +=1

        print('there was no solutions found!! Restart')


solver = GA(100, 2000)

solver.solver()
