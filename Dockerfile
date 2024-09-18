# Use Python runtime
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock to install dependencies
COPY pyproject.toml poetry.lock /app/

# Install poetry
RUN pip install poetry

# Install dependencies with poetry
RUN poetry install --no-root

# Copy the rest of the application code to the container
COPY . /app

# Expose the Streamlit port
EXPOSE 8501

# Set streamlit config
ENV STREAMLIT_CONFIG_DIR=/app/.streamlit

# Run the application
CMD ["poetry", "run", "streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]