# Use an official Python runtime as a parent image
FROM python:jessie

# Set the working directory to /app
WORKDIR .

# Copy the current directory contents into the container at /jibambe
ADD . /jibambe

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run jibambe.ini when the container launches
CMD ["uwsgi", "jibambe.ini"]