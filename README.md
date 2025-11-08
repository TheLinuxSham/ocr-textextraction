![Demo](/artefacts/pictures/demo-hello-world.png)

This service relies on multiple containerized components to extract text from images. It exposes an API for sending POST Requests with images to extract text from. This project leverages:
- [Tesseract](https://github.com/tesseract-ocr/tesseract) as an OCR Engine
- [FastApi](https://fastapi.tiangolo.com/) for compliance with [OpenApi](https://www.openapis.org/what-is-openapi) and ease of use
- [OpenCV](https://opencv.org/) to handle and process pictures
- [Python](https://www.python.org/) as a programming language

![Component Diagram of the service](/artefacts/pictures/component-diagram.png)

![Preview of the FastApi Website](/artefacts/pictures/fastapi-website.png)

# Prerequesites:
- Docker-Compose
- Docker
- Free space on disk
- Internet connection for downloading images

# Demo
This is a little demo with a sample picture sent to the service. It shows the response and gives a look at the accuracy.

The image:
![Demo picture for showing API response and accuracy](/artefacts/pictures/20251108_21h09m02s_grim.png)

The response:
```json
{
  "text": "having the ability to provide a definition of your api to other people - your colleagues, companies you partner with or organizations who you provide apis to - is vital to doing business. the success of the api economy is predicated on doing this repeatedly, succinctly and deterministically, using a vernacular that is relevant to the api consumer.",
  "version": 0.1,
  "details": {
    "duration": 0.5437,
    "job_id": "16d05ef13c3e45aeaed74466533c08cb",
    "filename": "20251108_21h09m02s_grim.png",
    "content_type": "image/png"
  },
  "errors": {
    "count": 0,
    "error": []
  }
}
```

The Api response is structured like this:

![Demo picture for showing API response and accuracy](/artefacts/pictures/api-response.png)

# How It Works

This is the flow from sending the picture to the service and receiving the result as json:
![Demo picture for showing API response and accuracy](/artefacts/pictures/sequence-diagram.png)

All pictures sent to the service undergo a series of preprocessing. This ensures best accuracy for most use cases with Tesseract. The steps are as follows:
1. convert the picture with rgb channels to grayscale
2. convert from grayscale to binary with otsu threshold
3. invert picture from darkmode to lightmode if necessary
4. evaluate font size and estimate rescaling factor for font size 30 and do scaling
5. apply gaussian blur
6. add a border of 10px all around

![Demo for image processing](/artefacts/pictures/demo-image-processing.png)

# Monitoring

The service comes with tools for monitoring, such as OpenTemeletry, Prometheus and Grafana. A template for Grafana can be found in the project:

![Demo for grafana dashboard](/artefacts/pictures/demo-grafana.png)

