# ChangeYourWalls
Allows to change the walls by the given pattern. This program aims to help with your interior update

![alt text](demo/results/5.jpg)

# Build a docker
```
docker build --build-arg UID="$(id -u)" --build-arg GID="$(id -g)" --build-arg UNAME="auto" -t mmseg_wall -f Dockerfile .

```

# Run docker and get segmentation mask for the image
```
docker run --rm -it --gpus all --net=host --ipc=host -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -v $HOME/.Xauthority:/home/auto/.Xauthority -v $PWD:/home/auto/ChangeYourWalls mmseg_wall
```

## Download the model and config
```
mim download mmsegmentation --config pspnet_r101-d8_480x480_80k_pascal_context_59 --dest models/
```

## Get the mask
```
python3 get_seg.py --obj_class wall
```

## get the pattern
```
python3 main.py
```
results are saved in `demo/results` dir