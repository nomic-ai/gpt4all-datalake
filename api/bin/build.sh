#!/usr/bin/env bash
set -e
set -x

AWS_ACCOUNT_ID='035920842895'
AWS_REGION='us-east-1'


if [ -z $1 ]; then
  echo "docker image name is required.."
  exit 1
fi

IMAGE_NAME="$1"; shift

while [[ $# -gt 0 ]]; do
  key="$1"
case $key in
    -t|--tag)
    tag="$2"
    shift
    ;;
    *)
    echo "Unknown flag: $key"
    exit 1
    ;;
  esac
  shift
done


if [ ! -z $tag ]; then
  DOCKER_TAG=$tag
else
  DOCKER_TAG="`date +%Y-%m-%d`"
fi

DOCKER_IMAGE_TAG=$IMAGE_NAME:$DOCKER_TAG

DOCKER_BUILDKIT=1 docker build -t $DOCKER_IMAGE_TAG --build-arg image_version="gpt4all_$(date +%y%m%d%H%M)" -f api/Dockerfile.buildkit .

echo "built image -> $DOCKER_IMAGE_TAG"
