# GitHub

The following repository contains all tools/code for Blue-Teams to audit code on GitHub

## secret-bridge

#### Running Via Docker
```
docker login docker.pkg.github.com -u USERNAME -p TOKEN
sudo docker run -ti -v $(pwd)/config.toml:/usr/src/app/config.toml docker.pkg.github.com/sorsnce/blue-team/secret-bridge:1.0 poll
```
