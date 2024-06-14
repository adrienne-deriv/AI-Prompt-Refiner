### Install

To run the project with Docker, build the image locally:

```
docker build -t ai-prompt-refiner ./
```

and run the image with:

```
docker run -p 8000:8000 -v "$(pwd)":/app ai-prompt-refiner
```
