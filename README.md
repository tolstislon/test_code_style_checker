# Test Code Style Checker

#### Use

```cmd
docker pull tolstislon/code-styler-api

# windows
docker run --rm -v $pwd/:/source_code tolstislon/code-styler-api

#linux
docker run --rm -v `pwd`/:/source_code tolstislon/code-styler-api
```


#### Dev

```cmd
# Local build
build.sh test

# Build and push
build.sh deploy
```