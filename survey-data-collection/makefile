up:
	docker-compose -f docker-compose.yml -p surveys_doc-gen_maze-group up -d --build

down:
	docker-compose -f docker-compose.yml -p surveys_doc-gen_maze-group down

rebuild:
	docker-compose -f docker-compose.yml -p surveys_doc-gen_maze-group build --no-cache fe

restart: down up
