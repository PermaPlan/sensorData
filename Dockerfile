FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

COPY src ./src
ADD data.db .
RUN mkdir ./logs

EXPOSE 5000
ENTRYPOINT ["conda", "run", "-n", "GP-sensorData", "python"]
CMD ["/app/src/server.py"]
