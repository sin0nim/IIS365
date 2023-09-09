# base image
FROM python:3-alpine
# загрузить все зависимости
RUN pip -r requirements.txt
# specify the port number the container should expose
EXPOSE 5000
# run the application
CMD ["flask", "run"]
