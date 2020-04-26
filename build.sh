#!/usr/bin/env bash
IMAGES="tolstislon/code-styler-api"

if [[ $1 == "test" ]]; then
  echo "Create test ${IMAGES}"
  docker build . -t ${IMAGES}
elif [[ $1 == "deploy" ]]; then
  image_tag=$(pipenv run python -c "import test_code_style_checker;print(test_code_style_checker.__version__)")
  echo "Create ${IMAGES}:${image_tag}"
  docker build . -t "${IMAGES}:${image_tag}"
  docker push "${IMAGES}:${image_tag}"
  docker rmi "${IMAGES}:${image_tag}"
else
  echo "Invalid agument: $1"
fi

# shellcheck disable=SC2162
read -p "Press enter to continue"
