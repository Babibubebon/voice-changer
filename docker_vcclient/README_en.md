## VC Client for Docker

[Japanese](/README_ja.md)

## Build

In root folder of repos.

```
npm run build:docker:vcclient
```

For AMD ROCm

```
npm run build:docker:vcclient:rocm
```

## preparation

Store weights of external models in `docker_vcclient/weights`. Which weights should be in the folder depends on which kind of VC you use.

```
$ tree docker_vcclient/weights/
docker_vcclient/weights/
├── checkpoint_best_legacy_500.onnx
├── checkpoint_best_legacy_500.pt
├── hubert-soft-0d54a1f4.pt
├── hubert_base.pt
└── nsf_hifigan
    ├── NOTICE.txt
    ├── NOTICE.zh-CN.txt
    ├── config.json
    └── model
```

## Run

In root folder of repos.

```
bash start_docker.sh
```

Without GPU

```
USE_GPU=off bash start_docker.sh
```

Specify port num

```
EX_PORT=<port> bash start_docker.sh
```

Use Local Image

```
USE_LOCAL=on bash start_docker.sh
```

For AMD ROCm

```
docker compose up -d && docker compose logs -f
```

## Push to Repo (only for devs)

```
npm run push:docker:vcclient
```
