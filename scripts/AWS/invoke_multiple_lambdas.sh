#!/bin/bash

# Payloads
PAYLOAD1='{"route": "GetMicroserviceDeploymentState", "fully_qualified_microservice_name": "platform-status-frontend.public.integration.mdtp", "ecs_deployment_id": "ecs-svc/8299622691673920999"}'
#PAYLOAD2='{"key2": "value2"}'
#PAYLOAD3='{"key3": "value3"}'

# Function to invoke Lambda
invoke_lambda() {
    local payload=$1
    aws lambda invoke --function-name "mdtp-lab03-build-and-deploy-proxy-lambda" \
                      --region "eu-west-2" \
                      --payload "$payload" \
                      response.json
    echo "Lambda invoked with payload: $payload"
    cat response.json
}

# Invoke Lambda with different payloads
invoke_lambda "$PAYLOAD1"
invoke_lambda "$PAYLOAD1"
invoke_lambda "$PAYLOAD1"
