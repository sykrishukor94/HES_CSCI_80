# Project 5: Traffic.py ReadMe

Syukri Shukor | CSCI E-80 | 17Apr2022

**Introduction**

In this assignment, we wish to improve a 
sub-optimal convolutional neural network (CNN) 
through a step-wise optimization process.
The metrics used to assess improved CNN model performance are as follows:

1) Minimize loss
2) Maximize accuracy
3) Model performance in testing > training data

**Design**

A step-wise optimization process was adopted to delineate the effects of various parameters.
All models were tested at least twice to confirm reproducibility and variance.

Once the effects of key parameters are determined in the first few rounds of testing, 
the best-performing model is further fine-tuned in subsequent rounds using a combination of parameters.

All testing models in each round can be found in **traffic.py**, using the **test_model_main()** as a driver function.

**Results**

The starting model - or 'default' model - was adapted from Lecture 5 CNN distribution code. 
It contains a convolution and pooling step, a hidden layer, and a dropout layer before the output.
```
    model = tf.keras.models.Sequential()
    model.add(keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)))  # 30x30 RGB images
    
    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(pool_size=(5, 5)))
    model.add(layers.Flatten())
    
    model.add(layers.Dense(128, activation="relu"))
    
    model.add(layers.Dropout(0.5))
    
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))
```

_Step-wise single-variable parameter testing_

In the first 2 round of testing, 14 models [1 - 14] were derived from the 'default' model 
to test the effects of various parameters outlined list below:

1) Different numbers of convolutional and pooling layers (CNP)
   1) 1 CNP **(default)**
   2) 3 CNPs without funneling [1]
   3) 5 CNPs with funneling [14]
2) Different numbers and sizes of filters for convolutional layers
   1) 32 filters **(default)**
      1) 3x3 kernel size **(default)**
      2) 5x5 kernel size [2]
      3) 10x10 kernel size [3]
   2) 3 filters
      1) 3x3 kernel size [4]
      2) 5x5 kernel size [5]
      3) 10x10 kernel size [6]
3) Different pool sizes for pooling layers
   1) 2x2 pool size [7]
   2) 3x3 pool size **(default)**
   3) 10x10 pool size [8]
4) Different numbers and sizes of hidden layers
   1) 1 hidden layer **(default)**
      1) 8 filters [9]
      2) 128 filters **(default)**
      3) 1024 filters [10]
   2) 3 hidden layers
      1) 8 filters [11]
      2) 128 filters [12]
   3) 5 hidden layers 
      1) 128 filters [13]
5) Dropout **(default)** versus no-dropout (tested in later optimization rounds)

From this round, the top 3 parameters that improved model performance were:
1) increasing number of convolutional layers and pooling (models [1] and [14])
2) increasing number and size of hidden layer (e.g models [10]. [11], [12])
3) increase number of pooling frame size (model [8])

As expected, reducing number of filters in either convolutional layer or in hidden layers worsened model performance.
Reducing pooling frame size also worsened model performance.

Model [1] is concluded as the best and was chosen for subsequent optimization. Comparing the 'default' model to model [1]:
1) improved loss function from ~3.5 to ~0.15 
2) improved accuracy from ~0.05 to ~0.95
3) testing > training model performance

_Improving model [1] by integrating top parameters_

Starting with the best model [1] from step-wise single-variable parameter testing:
    
    model = tf.keras.models.Sequential()
    model.add(keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)))  # 30x30 RGB images

    # 3 without funneling
    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(pool_size=(3, 3)))

    model.add(layers.Flatten())
    
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dropout(0.5))
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))

    # get model summary
    model.summary()
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

Model [1], which we set as **default** in this round of testing, is further optimized by:
1) adding hidden layers
   1) 1 hidden layer; 128 filter **(default)**
   2) 2 hidden layers; 128 filters each [1]
   3) 3 hidden layers; 64 filters each [2]
   4) 5 hidden layers; 16 filters each [3]
2) adding pooling layers
   1) 1 pooling layer **(default)**
   2) 2 pooling layer [4]
3) dropout **(default)** vs no-dropout [5]

From the above parameters tested, a model with 2 hidden layers (model [1]) saw the most improvement to the model, 
while reducing number of filters came at a detriment to model performance.
Comparing the **default** to model [1]:
1) Improved loss function from ~0.15 to ~0.07
2) Improved accuracy from ~0.95 to ~0.98
3) Comparable but mixed testing vs training performance over multiple runs

Implementing another CN and pooling layer in to model [1] in [4] led to a worsened performance.
This confirms that 1 pooling layer is sufficient. Once a somewhat optimal model was obtained, the effects 
of removing a dropout layer was tested.

Removing the dropout function in [5] on an optimized model led to a larger difference between 
model performance in testing and training data, where testing < training performance.
This observation suggests worsened overfitting in the non-dropout model. Thus, the dropout layer was chosen
to remain in the final model.

**Conclusion & Next Steps**

After a comprehensive testing and optimization with ~20 models, the final model chosen for implementation in 
the **get_model()** function is:
    
    # setup sequential CNN
    model = tf.keras.models.Sequential()

    # add input layer
    model.add(keras.Input(shape=(IMG_WIDTH, IMG_HEIGHT, 3)))  # 30x30 RGB images

    # add 3 CNN + 1 max pooling layers
    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.Conv2D(32, (3, 3), activation="relu"))
    model.add(layers.MaxPooling2D(pool_size=(3, 3)))

    model.add(layers.Flatten())

    # add 3 hidden layers
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dense(128, activation="relu"))
    model.add(layers.Dense(128, activation="relu"))

    # add dropout layer
    model.add(layers.Dropout(0.5))

    # add output layer
    model.add(layers.Dense(NUM_CATEGORIES, activation="softmax"))

    # get model summary
    model.summary()
    model.compile(
        optimizer="adam",
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )
    return model

In the future, multilayer, funnel-shaped convolution + pooling network approaches can be tested.
Reducing number of filters can also be explored to simplify the model and improve model runtime without sacrificing
performance. 
