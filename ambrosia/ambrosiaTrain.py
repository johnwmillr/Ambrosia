from __future__ import print_function

import sys
import os
import time
import csv

import numpy as np
import theano
import theano.tensor as T

import lasagne


# ################## Download and prepare the MNIST dataset ##################
# This is just some way of getting the MNIST dataset from an online location
# and loading it into numpy arrays. It doesn't involve Lasagne at all.

def load_dataset():

    # We first define a download function, supporting both Python 2 and 3.
    # if sys.version_info[0] == 2:
    #     from urllib import urlretrieve
    # else:
    #     from urllib.request import urlretrieve

    # def download(filename, source='http://yann.lecun.com/exdb/mnist/'):
    #     print("Downloading %s" % filename)
    #     urlretrieve(source + filename, filename)

    # # We then define functions for loading MNIST images and labels.
    # # For convenience, they also download the requested files if needed.
    # import gzip

    # def load_mnist_images(filename):
    #     if not os.path.exists(filename):
    #         download(filename)
    #     # Read the inputs in Yann LeCun's binary format.
    #     with gzip.open(filename, 'rb') as f:
    #         data = np.frombuffer(f.read(), np.uint8, offset=16)
    #     # The inputs are vectors now, we reshape them to monochrome 2D images,
    #     # following the shape convention: (examples, channels, rows, columns)
    #     data = data.reshape(-1, 1, 28, 28)
    #     # The inputs come as bytes, we convert them to float32 in range [0,1].
    #     # (Actually to range [0, 255/256], for compatibility to the version
    #     # provided at http://deeplearning.net/data/mnist/mnist.pkl.gz.)
    #     return data / np.float32(256)

    # def load_mnist_labels(filename):
    #     if not os.path.exists(filename):
    #         download(filename)
    #     # Read the labels in Yann LeCun's binary format.
    #     with gzip.open(filename, 'rb') as f:
    #         data = np.frombuffer(f.read(), np.uint8, offset=8)
    #     # The labels are vectors of integers now, that's exactly what we want.
    #     return data

    # We can now download and read the training and test set images and labels.

    with open('recipes_data_trimmed_features.csv') as dataFile:
        counter = 0
        datareader = csv.reader(dataFile)
        listformate = list(datareader)
        X_train = [] #substract the label column
        y_train = []
        X_test = [] #same
        y_test = []
        dataFile.seek(0)
        for row in datareader:
            if row[1] == '':
                row[1] = '0'
            row = [float(i) for i in row[1:]]
            if counter < len(listformate) * 0.9:
                X_train.append(row[1:])
                y_train.append(int(row[0]*2))
            else:
                X_test.append(row[1:])
                y_test.append(int(row[0])*2)
            counter += 1

    #y_train = np.array(y_train)
    #y_test = np.array(y_test)
    #y_train = np.transpose(y_train).flatten()
    #y_test = np.transpose(y_test).flatten()
    #y_test = y_test.tolist()
    #y_train = y_train.tolist()

    x_trainRow = len(X_train)
    # We reserve the last 10000 training examples for validation.
    X_train, X_val = X_train[:-int(x_trainRow*0.9)], X_train[-int(x_trainRow*0.9):]
    y_train, y_val = y_train[:-int(x_trainRow*0.9)], y_train[-int(x_trainRow*0.9):]

    # We just return all the arrays in order, as expected in main().
    # (It doesn't matter how we do this as long as we can read them again.)
    return X_train, y_train, X_val, y_val, X_test, y_test


# ##################### Build the neural network model #######################
# This script supports three types of models. For each one, we define a
# function that takes a Theano variable representing the input and returns
# the output layer of a neural network model built in Lasagne.

###################################################################################
###################################################################################
###################################################################################
### Essentially, it is saying that the optimal number of hidden nodes in the first 
### hidden layer is: sqrt[(m+2)N] + 2sqrt[N/(m+2)] and in the second hidden layer, 
### the optimal number of hidden nodes is: m*sqrt[N/(m+2)], where N = number of 
### inputs, and m = number of outputs
###################################################################################
###################################################################################
###################################################################################



def build_mlp(input_var=None):
    # This creates an MLP of two hidden layers of 800 units each, followed by
    # a softmax output layer of 10 units. It applies 20% dropout to the input
    # data and 50% dropout to the hidden layers.

    # Input layer, specifying the expected input shape of the network
    # (unspecified batchsize, 1 channel, 28 rows and 28 columns) and
    # linking it to the given Theano variable `input_var`, if any:
    l_in = lasagne.layers.InputLayer(shape=(None, 2908),input_var=input_var)

    # Apply 20% dropout to the input data:
    l_in_drop = lasagne.layers.DropoutLayer(l_in, p=0.2)

    # Add a fully-connected layer of 800 units, using the linear rectifier, and
    # initializing weights with Glorot's scheme (which is the default anyway):
    l_hid1 = lasagne.layers.DenseLayer(
            l_in_drop, num_units=350,
            nonlinearity=lasagne.nonlinearities.rectify,
            W=lasagne.init.GlorotUniform())

    # We'll now add dropout of 50%:
    l_hid1_drop = lasagne.layers.DropoutLayer(l_hid1, p=0.7)

    # Another 800-unit layer:
    l_hid2 = lasagne.layers.DenseLayer(
            l_hid1_drop, num_units=350,
            nonlinearity=lasagne.nonlinearities.rectify)

    # 50% dropout again:
    l_hid2_drop = lasagne.layers.DropoutLayer(l_hid2, p=0.7)

    # Finally, we'll add the fully-connected output layer, of 10 softmax units:
    l_out = lasagne.layers.DenseLayer(
            l_hid2_drop, num_units=11,
            nonlinearity=lasagne.nonlinearities.softmax)

    # Each layer is linked to its incoming layer(s), so we only need to pass
    # the output layer to give access to a network in Lasagne:
    return l_out





# ############################# Batch iterator ###############################
# This is just a simple helper function iterating over training data in
# mini-batches of a particular size, optionally in random order. It assumes
# data is available as numpy arrays. For big datasets, you could load numpy
# arrays as memory-mapped files (np.load(..., mmap_mode='r')), or write your
# own custom data iteration function. For small datasets, you can also copy
# them to GPU at once for slightly improved performance. This would involve
# several changes in the main program, though, and is not demonstrated here.
# Notice that this function returns only mini-batches of size `batchsize`.
# If the size of the data is not a multiple of `batchsize`, it will not
# return the last (remaining) mini-batch.

def iterate_minibatches(inputs, targets, batchsize, shuffle=False):
    assert len(inputs) == len(targets)
    inputs = np.array(inputs)
    targets = np.array(targets)
    if shuffle:
        indices = np.arange(len(inputs))
        np.random.shuffle(indices)
    for start_idx in range(0, len(inputs) - batchsize + 1, batchsize):
        if shuffle:
            excerpt = indices[start_idx:start_idx + batchsize]
        else:
            excerpt = slice(start_idx, start_idx + batchsize)

        yield inputs[excerpt], targets[excerpt]


# ############################## Main program ################################
# Everything else will be handled in our main program now. We could pull out
# more functions to better separate the code, but it wouldn't make it any
# easier to read.

def main(model='mlp', num_epochs=500):
    # Load the dataset
    print("Loading data...")
    X_train, y_train, X_val, y_val, X_test, y_test = load_dataset()
    print("done .. ")

    # Prepare Theano variables for inputs and targets
    input_var = T.matrix('inputs')
    target_var = T.ivector('targets')

    # Create neural network model (depending on first command line parameter)
    print("Building model and compiling functions...")
    if model == 'mlp':
        network = build_mlp(input_var)
    else:
        print("Unrecognized model type %r." % model)
        return

    # Create a loss expression for training, i.e., a scalar objective we want
    # to minimize (for our multi-class problem, it is the cross-entropy loss):
    prediction = lasagne.layers.get_output(network)
    loss = lasagne.objectives.categorical_crossentropy(prediction, target_var)
    loss = loss.mean()
    # We could add some weight decay as well here, see lasagne.regularization.

    # Create update expressions for training, i.e., how to modify the
    # parameters at each training step. Here, we'll use Stochastic Gradient
    # Descent (SGD) with Nesterov momentum, but Lasagne offers plenty more.
    params = lasagne.layers.get_all_params(network, trainable=True)
    updates = lasagne.updates.nesterov_momentum(
            loss, params, learning_rate=0.001, momentum=0.9)

    # Create a loss expression for validation/testing. The crucial difference
    # here is that we do a deterministic forward pass through the network,
    # disabling dropout layers.
    test_prediction = lasagne.layers.get_output(network, deterministic=True)
    test_loss = lasagne.objectives.categorical_crossentropy(test_prediction,target_var)
    test_loss = test_loss.mean()
    # As a bonus, also create an expression for the classification accuracy:
    test_acc = T.mean(T.eq(T.argmax(test_prediction, axis=1), target_var),dtype=theano.config.floatX)

    # Compile a function performing a training step on a mini-batch (by giving
    # the updates dictionary) and returning the corresponding training loss:
    train_fn = theano.function([input_var, target_var], loss, updates=updates, allow_input_downcast=True)

    # Compile a second function computing the validation loss and accuracy:
    val_fn = theano.function([input_var, target_var], [test_loss, test_acc], allow_input_downcast=True)

    # Finally, launch the training loop.
    print("Starting training...")
    # We iterate over epochs:
    for epoch in range(num_epochs):
        # In each epoch, we do a full pass over the training data:
        train_err = 0
        train_batches = 0
        start_time = time.time()
        for batch in iterate_minibatches(X_train, y_train, 500, shuffle=True):
            inputs, targets = batch
            print(inputs.shape)
            print(targets.shape)
            train_err += train_fn(inputs, targets)
            train_batches += 1

        # And a full pass over the validation data:
        val_err = 0
        val_acc = 0
        val_batches = 0
        for batch in iterate_minibatches(X_val, y_val, 500, shuffle=False):
            inputs, targets = batch
            err, acc = val_fn(inputs, targets)
            val_err += err
            val_acc += acc
            val_batches += 1

        # Then we print the results for this epoch:
        print("Epoch {} of {} took {:.3f}s".format(
            epoch + 1, num_epochs, time.time() - start_time))
        print("  training loss:\t\t{:.6f}".format(train_err / train_batches))
        print("  validation loss:\t\t{:.6f}".format(val_err / val_batches))
        print("  validation accuracy:\t\t{:.2f} %".format(
            val_acc / val_batches * 100))

    # After training, we compute and print the test error:
    test_err = 0
    test_acc = 0
    test_batches = 0
    for batch in iterate_minibatches(X_test, y_test, 500, shuffle=False):
        inputs, targets = batch
        err, acc = val_fn(inputs, targets)
        test_err += err
        test_acc += acc
        test_batches += 1
    print("Final results:")
    print("  test loss:\t\t\t{:.6f}".format(test_err / test_batches))
    print("  test accuracy:\t\t{:.2f} %".format(
        test_acc / test_batches * 100))

    # Optionally, you could now dump the network weights to a file like this:
    # np.savez('model.npz', *lasagne.layers.get_all_param_values(network))
    #
    # And load them again later on like this:
    # with np.load('model.npz') as f:
    #     param_values = [f['arr_%d' % i] for i in range(len(f.files))]
    # lasagne.layers.set_all_param_values(network, param_values)


if __name__ == '__main__':
    if ('--help' in sys.argv) or ('-h' in sys.argv):
        print("Trains a neural network on MNIST using Lasagne.")
        print("Usage: %s [MODEL [EPOCHS]]" % sys.argv[0])
        print()
        print("MODEL: 'mlp' for a simple Multi-Layer Perceptron (MLP),")
        print("       'custom_mlp:DEPTH,WIDTH,DROP_IN,DROP_HID' for an MLP")
        print("       with DEPTH hidden layers of WIDTH units, DROP_IN")
        print("       input dropout and DROP_HID hidden dropout,")
        print("       'cnn' for a simple Convolutional Neural Network (CNN).")
        print("EPOCHS: number of training epochs to perform (default: 500)")
    else:
        kwargs = {}
        if len(sys.argv) > 1:
            kwargs['model'] = sys.argv[1]
        if len(sys.argv) > 2:
            kwargs['num_epochs'] = int(sys.argv[2])
        main(**kwargs)