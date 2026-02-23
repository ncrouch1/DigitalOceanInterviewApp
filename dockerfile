FROM python:3.13
WORKDIR /usr/local/app

RUN cd /usr/local/app
RUN python3 -m venv venv
RUN source venv/bin/activate

# Install the application dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy in the source code
COPY src ./src
EXPOSE 8080

# Setup an app user so the container doesn't run as the root user
RUN useradd app
USER app

CMD ["fastapi", "run", "/usr/local/app/main.py", "--port", "8080"]
