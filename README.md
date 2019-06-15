# Mushroom blog
This is a practice for hosting a blog app

## Setup
The stack is fully containerised, if under linux/mac environment, you can simply use 
```bash
$ make run
```
under the hood, it first build by running
```bash
$ ./docker/build.sh # a shellscript build all relevant docker images
$ ./localstack up # another shellscript uses docker-compose to setup a local stack
```
