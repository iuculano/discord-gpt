FROM python:slim
ENV OPENAI_API_KEY=replace_me
ENV DISCORD_BOT_TOKEN=replace_me
COPY ./src requirements.txt ./

RUN pip install -r requirements.txt
CMD ["python3", "./main.py"]
