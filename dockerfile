FROM python:3.13

# 1. Set the working directory
WORKDIR /usr/local/app

# 2. Install dependencies directly to the system Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy your source code (maintaining the 'src' folder structure)
COPY . ./src

# 4. Expose the port
EXPOSE 8080

# 5. Setup and switch to a non-root user
RUN useradd -m app
USER app

# 6. Start the app. 
# Note the path: if main.py is inside the 'src' folder, reference it as 'src/main.py'
CMD ["honcho", "start"]
