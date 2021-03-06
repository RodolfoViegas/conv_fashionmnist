import tensorflow as tf
print(tf.__version__)
mnist = tf.keras.datasets.mnist
(training_images, training_labels), (test_images, test_labels) = mnist.load_data()


#Callback
class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.995):
      print("\nReached 99% accuracy so cancelling training!")
      self.model.stop_training = True

callbacks = myCallback()


#Separação do conjunto de validação
valid_images = training_images[:10000]
valid_images = valid_images.reshape(10000, 28, 28, 1)
valid_images = valid_images / 255.0
valid_labels = training_labels[:10000]


# Formalização do conjunto de treino
training_images = training_images[10000:]
training_images = training_images.reshape(50000, 28, 28, 1)
training_images = training_images / 255.0
training_labels = training_labels[10000:]



test_images = test_images.reshape(10000, 28, 28, 1)
test_images=test_images/255.0


model = tf.keras.models.Sequential([
  tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28, 28, 1)),
  tf.keras.layers.MaxPooling2D(2, 2),
  
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(training_images, training_labels, epochs=12,  callbacks=[callbacks], validation_data=(valid_images, valid_labels))
test_loss, test_acc = model.evaluate(test_images, test_labels)


print("Acurácia da rede no conjunto de teste",test_acc) 
