FROM python:3.8.5

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install missing libs for opencv
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Make port 3000 and 5000 available to the world outside this container
EXPOSE 3000
EXPOSE 5000

# Run multiple app.py when the container launches
# the app.py are in folders ai_gateway, ai_server, server
CMD ["sh", "runner.sh"]
