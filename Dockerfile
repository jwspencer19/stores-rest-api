# Use an official Python runtime as a parent image
FROM python

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
# RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV NAME="Rest Section 6"
# ENV DATABASE_URL=postgresql://postgres:docker@bosspencerj:5432/postgres

# Run app.py when the container launches
CMD ["python", "app.py"]
