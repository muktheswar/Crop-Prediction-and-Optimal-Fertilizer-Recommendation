FROM continuumio/miniconda3

WORKDIR /

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "crop_pred", "/bin/bash", "-c"]

# Activate the environment, and make sure it's activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
COPY app.py .
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "crop_pred", "python", "app.py"]