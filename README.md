# guane-technical-skill-test


mysecretpassword

# Run
1. api auth: uvicorn main:app --port 8083 --reload
2. api animal management uvicorn main:app --port 8084 --reload
3. rabbitmq => docker run --rm -it --hostname rabbit-container -p 15672:15672 -p 5672:5672 --name rabbitmq-container rabbitmq:3-management

Nota: show queues http://localhost:15672/ user:guest passw: guest
4. celery api: uvicorn main:app --port 8085 --reload
5. Start celery: celery -A task.celery_app worker -l info -Q email_to_send
6. api gatewat => uvicorn main:app --port 8086 --reload


# Que se

1. passlib y el algoritmo Bcrypt para el hash de las passwords
2. openssl para la generación del SECRET KEY con el comando  openssl rand -hex 32
3. se guardaron las variables en un archivo .env
4. se usaron ramas como develop y main , cada funcionalidad se trabajo como una rama independiente.
