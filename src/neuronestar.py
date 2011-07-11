#!/Users/Gecko/Documents/pypy-c-jit-bin/bin/pypy

#import sys
import pickle

from math import tanh, sqrt
from random import random
    


# get a random number where:  a <= rand < b
randRange = lambda a, b : (b - a) * random() + a
# our sigmoid function, tanh is a little nicer than the standard 1/(1+e^-x)
def sigmoid(x): return tanh(x)
# derivative of our sigmoid function
def dsigmoid(y): return 1.0 - y ** 2
    
   
#Un neurone est une structure tres simple    
class Neuron(object):
    def __init__(self, ni, w=None):
        self.ni = ni #nombre d'entrees
        if w is not None:
            #des poids initiaux peuvent etre fournis
            self.weights = w
        else:
            #initialisation aleatoire des poids
            self.weights = [randRange(-1, 1) for a in range(self.ni)] 
        self.a = 0.0 #dernier poid calcule
        self.c = [0.0] * len(self.weights) #dernier changement des poids



class Perceptron:
    # number of input, hidden, output nodes, learning rate
    def __init__(self, ni, nh_list, no, rate=0.05, momentum=0.1):
        assert 0 < rate < 1, "Bad learning rate"
        assert 0 < momentum < 1, "Bad momentum value"
        self.learning_rate = rate
        self.momentum = momentum #less oscillations
        #input layer
        self._inputs = [Neuron(1, [randRange(-0.2, 0.2)]) for h in range(ni)]
        self._inputs.append(Neuron(1, [1.0])) #bias
        #hidden layers
        self._hiddens = []
        if len(nh_list) > 0:
            self._hiddens = [[Neuron(ni,) for h in range(nh_list[0])]]
            _last_nh = len(self._hiddens[0])
            for nh in nh_list[1:]:
                # intervalle d'initialisation des poids
                r = sqrt(6. / (_last_nh + nh))
                # creation de la couche de neurones intermediaires
                self._hiddens += [[Neuron(_last_nh, [randRange(-r, r) for a in range(_last_nh)]) 
                                    for h in range(nh)] ]
                _last_nh = nh
        else:
            _last_nh = ni
        #output layer
        self._outputs = [Neuron(no, [randRange(-0.2, 0.2) for a in range(_last_nh)]) for h in range(no)]

    def compute(self, inputs):
        assert len(inputs) == len(self._inputs) - 1, "Wrong number of inputs"
        #set inputs values from parameter
        for i, _input in enumerate(self._inputs[:-1]):
            _input.a = inputs[i] 
        #compute hidden values  
        _src_layer = self._inputs[:-1]
        for hidden_layer in self._hiddens:
            for j, hidden in enumerate(hidden_layer):
                g = sum([src_neuron.a * hidden.weights[i] for i, src_neuron in enumerate(_src_layer)])
                hidden.a = sigmoid(g)
            #next data            
            _src_layer = hidden_layer
        #compute output values
        _src_layer = self._hiddens[-1] if len(self._hiddens) > 0 else self._inputs[:-1]
        for output in self._outputs:
            g = sum([hidden.a * output.weights[i] for i, hidden in enumerate(_src_layer)])
            output.a = sigmoid(g)  
             
        return [output.a for output in self._outputs]

    def _updateWeights(self, src, dest, dest_errors):
        _learning_rate, _momentum = self.learning_rate, self.momentum
        for i, s in enumerate(src):
            src_neuron_value = s.a
            for k, d in enumerate(dest):
                change = dest_errors[k] * src_neuron_value
                #l'apprentissage se fait ici
                d.weights[i] += _learning_rate * change + _momentum * d.c[i]
                d.c[i] = change

    def backPropagate(self, targets):
        assert len(targets) == len(self._outputs), 'Wrong number of target values'
        # calculate error terms for output
        _output_deltas = [dsigmoid(o.a) * (targets[k] - o.a) for k, o in enumerate(self._outputs)]  
        # calculate error terms for the hidden layers
        _src_deltas = _output_deltas
        _src_layer = self._outputs
        _hidden_deltas = []
        for hidden_layer in self._hiddens[-1::-1]:
            _deltas = [dsigmoid(hidden.a) * sum([_src_deltas[k] * o.weights[j] for k, o in enumerate(_src_layer)]) 
                                 for j, hidden in enumerate(hidden_layer)]
            _hidden_deltas.append(_deltas)
            #next data
            _src_deltas = _deltas
            _src_layer = hidden_layer
        
        #update weights
        _deltas = _output_deltas
        _dest = self._outputs
        for i, hidden_layer in enumerate(self._hiddens[-1::-1]):
            self._updateWeights(hidden_layer, _dest, _deltas)
            #next data
            _deltas = _hidden_deltas[-i]
            _dest = hidden_layer
        
        if len(self._hiddens) > 0:    
            #update weights of the first hidden layer                          
            self._updateWeights(self._inputs[:-1], self._hiddens[0], _deltas)
        else:
            #update only the weights of the output layer (no hidden layer at all)                          
            self._updateWeights(self._inputs[:-1], self._outputs, _deltas)             
        #compute the error from target and output values then return it
        return sum([0.5 * (targets[k] - output.a) ** 2 for k, output in enumerate(self._outputs)])


    def train(self, patterns, max_iterations=750, error_threshold=0.02):
        _nb_iter = 0
        _error = 1.0
        _initial_rate = self.learning_rate
        _backPropagate = self.backPropagate
        _compute = self.compute
        while _nb_iter < max_iterations and _error > error_threshold:
            _nb_iter += 1
            _error = 0.0
            for inputs, targets in patterns:
                #compute values
                _compute(inputs)
                #update weights
                _error += _backPropagate(targets)
            if self.learning_rate >= 0.02:
                self.learning_rate = _initial_rate - _initial_rate * (_nb_iter / max_iterations) 
            else:
                self.learning_rate = _initial_rate

        #self.learning_rate = _initial_rate
        return (_nb_iter, _error)
     
    def computeFromPattern(self, patterns):
        for p in patterns:
            print ["%-.4f" % s for s in p[0]], ' --> ',
            print ["%-.4f" % s for s in self.compute(p[0])], '  :  ',
            print ["%-.4f" % s for s in p[1]]



import time

def demo(pat, ni, nh_list, no):
    for p in pattern:
        print ["%-.4f" % s for s in p[0]], ' --> ',
        print ["%-.4f" % s for s in p[1]]
    
    print ""
    
    # create a network and train it with some patterns
    resetPerceptron = lambda : Perceptron(ni, nh_list, no)
    print "=" * 90, "\nstarting the training...\n", "="*90, "\n",
    p = resetPerceptron()
    last_error, error = 0, 1
    nb_iter = 0
    total_iter = 0
    MAX_ITER = 850
    ERROR_THRESHOLD = 0.0035
    start_time = time.time()
    
    #data for the matplot graph
    x, y = [], []
    
    while error >= ERROR_THRESHOLD and abs(error - last_error) > 0.000001:

        last_error = error
        (itr, error) = p.train(pat, MAX_ITER, ERROR_THRESHOLD)
        total_iter += itr
        
        x.append(total_iter)
        y.append(error)

        if error > 0.22:
            print "ERROR: %-.6f  -->  resetting with new random weights..." % error
            nb_iter = 0
            total_iter = 0
            x = []
            y = []
            p = resetPerceptron()
        else:
            nb_iter += 1
            print "    %i)  iterations: %i   error: %-.6f" % (nb_iter, total_iter, error)


    
    print "\n", "="*90, "\ntest of the pattern: \n", "="*90, "\n" 
    p.computeFromPattern(pat)
    print "\ntotal time: %-.2f" % (time.time() - start_time), "seconds"
    print "total iterations: %i" % total_iter
    print "final error: %-.4f\n" % error
    

    print "writing the data to a file...",
    try:
        with open("perceptron.dump", "w") as f:
            pickle.dump(p, f)
            print " done.\n" 
    except Exception:
        print " error, data not saved.\n" 
          
    
    return (x, y)
    
    
    
    


if __name__ == '__main__':
    
    #import psyco
    #psyco.full()   
    

    def clamp(value, a, b):
        if a > b: b, a = a, b
        if value <= a: return a
        if value >= b: return b
        return value

        
    v = [1.0, 0.5, 0]
    combi = [(a, b, c) for a in v for b in v for c in v]
    pattern = []
    
    for (a, b, c)  in combi:
        pat = (
               (a + random() / 50., b + random() / 50., c + random() / 50.), #add noise to the three inputs
               (clamp(a - 1 + 1.70 * b + c - 1, 0, 1), clamp((c - a), -1, 1)) #speed, delta angle
              )
        
        pattern.append(pat)

    graph_x, graph_y = demo(pattern, 3, [8, 8], 2)

        
    try:
        import pylab
    except:
        print "Warning: Cannot import pylab ---> no graphic output will be made from the data"
    else:
        pattern = set(pattern)
        pattern.add(((1, 1, 1), (1, 0)))
        #3 inputs, 2x8 hidden, 2 output (speed, delta angle)
        
        print graph_x, graph_y
        pylab.xlabel("training iterations")
        pylab.ylabel("error rate")
        pylab.grid(True)
        pylab.autoscale(axis="x", tight=True)
        
        pylab.plot(graph_x, graph_y, color="green")
        pylab.plot(graph_x, graph_y, 'ro')
        pylab.title('Error rate over time')
        pylab.savefig("perceptron_training.png")
        pylab.show()
        
