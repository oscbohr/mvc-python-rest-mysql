# set base image (host OS)
FROM python:3.8.10

# set the working directory in the container
WORKDIR /app

COPY /meli-procesar-archivo/codigo/ /app/

# copy the dependencies file to the working directory
COPY /meli-procesar-archivo/codigo/requirements.txt .

# install dependencies
RUN pip install -r requirements.txt

# copy the all content of directory to the working directory
#COPY . .

RUN ls /app
ENV FLASK_ENV=development
CMD ["python3", "app.py"]