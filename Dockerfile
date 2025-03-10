FROM docker.1ms.run/conda/miniconda3:latest

WORKDIR /app

COPY . .

RUN conda create -n artex python=3.9.0 -y && \
conda init bash && \
. ~/.bashrc && \
conda activate artex && \
conda install -c bioconda artex && \
artex --version && \
artex --help && \
artex --test && \
echo "Artex test success" && \
echo "conda activate artex" >> ~/.bashrc && \
. ~/.bashrc && \
echo "Auto activate written to bashrc"

WORKDIR /root



