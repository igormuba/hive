#!/bin/bash

docker container stop $(docker container ls -q --filter name=hived)
docker container prune -f
docker image prune -f
docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
docker pull $CI_REGISTRY_IMAGE/consensus_node:$CI_COMMIT_SHORT_SHA
docker run -d -p 2001:2001 -p 8090:8090 --name hived --restart unless-stopped $CI_REGISTRY_IMAGE/consensus_node:$CI_COMMIT_SHORT_SHA
docker logout
