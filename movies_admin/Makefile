include .env
export $(shell sed 's/=.*//' .env)

.PHONY: build run stop restart shell logs clean \
	check_network create-network copy-static run-nginx run-uwsgi


# Сборка Docker-образа
build:
	docker build \
		--build-arg SECRET_KEY="$(SECRET_KEY)" \
		--build-arg DEBUG="$(DEBUG)" \
		-t $(IMAGE_NAME) .

# Запуск контейнера с подключением к БД в контейнере на этом же сервере
run: check_network create-network
	docker network inspect $(DB_NETWORK_NAME) >/dev/null 2>&1 || \
		docker network create $(DB_NETWORK_NAME)
	docker run --rm --name $(CONTAINER_NAME) --network=$(DB_NETWORK_NAME) \
		--network app_network --network-alias $(CONTAINER_NAME) \
		-p $(PORT):8000 \
		-e "SECRET_KEY=$(SECRET_KEY)" \
		-e "DEBUG=$(DEBUG)" \
		-e "DB_NAME=$(DB_NAME)" \
		-e "DB_USER=$(DB_USER)" \
		-e "DB_PASSWORD=$(DB_PASSWORD)" \
		-e "DB_HOST=$(DB_HOST)" \
		-e "DB_PORT=$(DB_PORT)" \
		-e "ALLOWED_HOSTS=$(ALLOWED_HOSTS)" \
		-e "INTERNAL_IPS=$(INTERNAL_IPS)" \
		$(IMAGE_NAME)

# Запуск приложения с удаленной БД
run-db-remote create-network:
	docker run --rm -d --name $(CONTAINER_NAME) \
		--network app_network --network-alias $(CONTAINER_NAME) \
		-p $(PORT):8000 \
		-e "SECRET_KEY=$(SECRET_KEY)" \
		-e "DEBUG=$(DEBUG)" \
		-e "DB_NAME=$(DB_NAME)" \
		-e "DB_USER=$(DB_USER)" \
		-e "DB_PASSWORD=$(DB_PASSWORD)" \
		-e "DB_HOST=$(DB_HOST)" \
		-e "DB_PORT=$(DB_PORT)" \
		-e "ALLOWED_HOSTS=$(ALLOWED_HOSTS)" \
		-e "INTERNAL_IPS=$(INTERNAL_IPS)" \
		$(IMAGE_NAME)


# Остановка и удаление контейнера
stop:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Перезапуск контейнера
restart: stop run

# Открыть оболочку внутри контейнера
shell:
	docker exec -it $(CONTAINER_NAME) sh

# Просмотр логов контейнера
logs:
	docker logs -f $(CONTAINER_NAME)

clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true
	docker ps -a --filter "ancestor=$(IMAGE_NAME)" --format "{{.ID}}" | xargs -r docker stop || true
	docker ps -a --filter "ancestor=$(IMAGE_NAME)" --format "{{.ID}}" | xargs -r docker rm || true
	#docker rmi $(IMAGE_NAME) || true

# Проверка наличия сети
check_network:
	@if ! docker network inspect $(DB_NETWORK_NAME) >/dev/null 2>&1; then \
		echo "Error: Network $(DB_NETWORK_NAME) not found."; \
		echo "Please create the network and attach the database to it:"; \
		echo "    docker network create $(DB_NETWORK_NAME)"; \
		exit 1; \
	fi

create-network:
	docker network inspect app_network >/dev/null 2>&1 || docker network create app_network

copy-static:
	docker cp $(CONTAINER_NAME):/var/www/static ./static

run-nginx:
	@if docker ps -a --filter "name=nginx" --format "{{.Names}}" | grep -w nginx >/dev/null; then \
		docker stop nginx >/dev/null; \
		docker rm nginx >/dev/null; \
	fi
	echo "CONTAINER_NAME=$(CONTAINER_NAME)"
	echo "PORT=$(PORT)"
	envsubst '$$CONTAINER_NAME $$PORT' < $(PWD)/django-ng.conf > $(PWD)/temp-django.conf
	cat $(PWD)/temp-django.conf
	docker run --rm --name nginx \
		--network app_network \
		-p 80:80 \
		--mount type=bind,source=$(PWD)/temp-django.conf,target=/etc/nginx/conf.d/django.conf,readonly \
		--mount type=bind,source=$(PWD)/static,target=/static,readonly \
		nginx:latest
	rm -f $(PWD)/temp-django.conf

run-uwsgi:
	echo $(shell pwd)/static
	uwsgi --module=config.wsgi --http :8000 --static-map /static=$(shell pwd)/static

