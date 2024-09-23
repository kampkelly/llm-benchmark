#!/bin/bash

set -a
source .env
set +a

cd ./llm-benchmark-chart

helm dependency update

cd ..

# Generate a values file from .env
cat <<EOF > llm-benchmark-chart/values-overrides.yaml
secrets:
  POSTGRES_PASSWORD: "$POSTGRES_PASSWORD"
  API_KEY: "$API_KEY"
EOF

helm upgrade --install llm-benchmark ./llm-benchmark-chart \
  --values llm-benchmark-chart/values-overrides.yaml
