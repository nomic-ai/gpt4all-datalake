set -e
set -x

AWS_ACCOUNT_ID='035920842895'
AWS_REGION='us-east-1'


if [ -z $1 ]; then
  echo "docker image name is required.."
  exit 1
fi

IMAGE_NAME="$1"; shift


if [ -z $1 ]; then
  echo "docker image tag is required.."
  exit 1
fi


DOCKER_TAG="$1"; shift


if [ -n "$1" ]; then
  WORKSPACE_TAG=$1
else
  if [ -v CIRCLE_BRANCH ]; then
    echo "determine workspace by circle branch: $CIRCLE_BRANCH"
    if [ "$CIRCLE_BRANCH" == "main" ]; then
      WORKSPACE_TAG='dev'
    else
      WORKSPACE_TAG=$CIRCLE_BRANCH
    fi
  else
    WORKSPACE_TAG='dev'
  fi
fi


echo "workspace is $WORKSPACE_TAG"
ECR_ENDPOINT_URL="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

echo "ecr endpoint: ($ECR_ENDPOINT_URL)"

docker tag $IMAGE_NAME:$DOCKER_TAG $ECR_ENDPOINT_URL/$IMAGE_NAME:$DOCKER_TAG

docker tag $IMAGE_NAME:$DOCKER_TAG $ECR_ENDPOINT_URL/$IMAGE_NAME:$WORKSPACE_TAG

# login to aws ecr.
$(aws ecr get-login --no-include-email)

docker push $ECR_ENDPOINT_URL/$IMAGE_NAME:$DOCKER_TAG
echo "pushed: $ECR_ENDPOINT_URL/$IMAGE_NAME$DOCKER_TAG.."

docker push $ECR_ENDPOINT_URL/$IMAGE_NAME:$WORKSPACE_TAG
echo "pushed: $ECR_ENDPOINT_URL/$IMAGE_NAME:$WORKSPACE_TAG.."