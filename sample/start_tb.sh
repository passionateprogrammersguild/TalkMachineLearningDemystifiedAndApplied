rm -rf /tmp/mnist_logs
tensorboard --logdir=/tmp/mnist_logs &
firefox http://0.0.0.0:6006 &