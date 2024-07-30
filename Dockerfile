FROM python
WORKDIR app/
COPY ./server app/
COPY terraform /usr/bin/terraform
RUN pip install --no-cache-dir -r app/requirements.txt
EXPOSE 5000
CMD ["python", "app/app.py"]

